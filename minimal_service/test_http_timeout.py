"""Real-loopback HTTP regressions for the CERBERUS socket timeout patch.

Run from the repository root:
    python -m unittest minimal_service.test_http_timeout -v

Standard library only. No worker, source retrieval or external network calls.
The suite must run serially because the service reads process environment.
Most tests use a 0.25-second handler subclass; one tests the real 10-second
setting. Production source and Handler.timeout are never modified.
"""
import http.client
import json
import os
from pathlib import Path
import socket
import sqlite3
import tempfile
import threading
import time
import traceback
import unittest
from unittest.mock import patch

from minimal_service import service

TOKEN = 'synthetic-timeout-regression-token-00000000'
FAST_TIMEOUT = 0.25
CLIENT_TIMEOUT = 3.0


class RecordingServer(service.HTTPServer):
    def __init__(self, address, handler):
        self.accepted = threading.Event()
        self.finished = threading.Event()
        self.responses = []
        self.errors = []
        super().__init__(address, handler)

    def handle_error(self, request, client_address):
        self.errors.append(traceback.format_exc())


class ObservedHandler(service.Handler):
    def setup(self):
        super().setup()
        self.server.accepted.set()

    def finish(self):
        try:
            super().finish()
        finally:
            self.server.finished.set()

    def respond(self, code, result):
        self.server.responses.append(code)
        return super().respond(code, result)


class FastHandler(ObservedHandler):
    timeout = FAST_TIMEOUT


class TimeoutRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='cerberus-http-timeout-')
        self.addCleanup(self.tmp.cleanup)
        self.db_path = Path(self.tmp.name) / 'research.sqlite'
        env = patch.dict(os.environ, {
            'CERBERUS_DB': str(self.db_path), 'CERBERUS_TOKEN': TOKEN})
        env.start()
        self.addCleanup(env.stop)
        db = service.connect()
        db.close()
        self.server = None
        self.thread = None
        self.clients = []
        self.addCleanup(self.stop_server)

    def stop_server(self):
        for client in self.clients:
            try:
                client.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            client.close()
        if self.server is not None:
            # Closing clients first releases any handler still waiting for input.
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(timeout=3)
            self.assertFalse(self.thread.is_alive(), 'Server thread did not stop')
            self.assertEqual(self.server.errors, [], 'Unhandled server exception')

    def start_server(self, handler=FastHandler):
        self.server = RecordingServer(('127.0.0.1', 0), handler)
        self.thread = threading.Thread(
            target=self.server.serve_forever,
            kwargs={'poll_interval': 0.02}, daemon=True)
        self.thread.start()

    def connect_client(self, timeout=CLIENT_TIMEOUT):
        self.server.accepted.clear()
        self.server.finished.clear()
        client = socket.create_connection(self.server.server_address, timeout=timeout)
        client.settimeout(timeout)
        self.clients.append(client)
        self.assertTrue(self.server.accepted.wait(2), 'Handler did not accept client')
        return client

    def assert_empty_database(self):
        with sqlite3.connect(self.db_path) as db:
            for table in ('requests', 'jobs', 'evidence', 'products'):
                self.assertEqual(db.execute('SELECT COUNT(*) FROM ' + table).fetchone()[0], 0, table)

    def assert_timeout_close(self, client):
        try:
            received = client.recv(4096)
        except socket.timeout:
            self.fail('Server failed to close the inactive connection')
        self.assertEqual(received, b'', 'Timed-out handler unexpectedly wrote a response')
        self.assertTrue(self.server.finished.wait(2), 'Handler cleanup did not finish')
        self.assertEqual(self.server.responses, [])
        self.assert_empty_database()

    def headers(self, size):
        return (f'POST /requests HTTP/1.1\r\nHost: localhost\r\n'
                f'Authorization: Bearer {TOKEN}\r\nContent-Type: application/json\r\n'
                f'Content-Length: {size}\r\nConnection: close\r\n\r\n').encode()

    def valid_body(self):
        return json.dumps({'question': 'Synthetic timeout test',
                           'sources': ['https://example.org/']}).encode()

    def post_valid(self, token=TOKEN):
        conn = http.client.HTTPConnection(*self.server.server_address, timeout=CLIENT_TIMEOUT)
        try:
            conn.request('POST', '/requests', body=self.valid_body(),
                         headers={'Authorization': 'Bearer ' + token,
                                  'Content-Type': 'application/json',
                                  'Connection': 'close'})
            response = conn.getresponse()
            return response.status, json.loads(response.read())
        finally:
            conn.close()

    def test_default_configuration_remains_ten_seconds(self):
        self.assertEqual(service.CLIENT_SOCKET_TIMEOUT, 10)
        self.assertEqual(service.Handler.timeout, 10)
        self.assertEqual(ObservedHandler.timeout, 10)

    def test_default_timeout_closes_idle_connection(self):
        self.start_server(ObservedHandler)
        client = self.connect_client(timeout=13)
        start = time.monotonic()
        self.assert_timeout_close(client)
        elapsed = time.monotonic() - start
        self.assertGreaterEqual(elapsed, 8.0)
        self.assertLess(elapsed, 13.0)

    def test_idle_connection_closes_before_request_line(self):
        self.start_server()
        self.assert_timeout_close(self.connect_client())

    def test_incomplete_headers_time_out(self):
        self.start_server()
        client = self.connect_client()
        client.sendall(b'POST /requests HTTP/1.1\r\nHost: localhost\r\nX-Incomplete:')
        self.assert_timeout_close(client)

    def test_stalled_authenticated_body_times_out_without_response(self):
        self.start_server()
        client = self.connect_client()
        body = self.valid_body()
        client.sendall(self.headers(len(body)) + body[:8])
        self.assert_timeout_close(client)

    def test_truncated_body_returns_400_and_does_not_insert(self):
        self.start_server()
        client = self.connect_client()
        body = self.valid_body()
        # Syntactically valid JSON still cannot be accepted when framing is short.
        client.sendall(self.headers(len(body) + 10) + body)
        client.shutdown(socket.SHUT_WR)
        response = http.client.HTTPResponse(client)
        response.begin()
        self.assertEqual(response.status, 400)
        self.assertEqual(json.loads(response.read()), {'error': 'Incomplete request body'})
        response.close()
        self.assertTrue(self.server.finished.wait(2))
        self.assertEqual(self.server.responses, [400])
        self.assert_empty_database()

    def test_valid_authenticated_request_still_succeeds(self):
        self.start_server()
        status, result = self.post_valid()
        self.assertEqual(status, 201)
        self.assertIn('request_id', result)
        with sqlite3.connect(self.db_path) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM requests').fetchone()[0], 1)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM jobs').fetchone()[0], 1)

    def test_invalid_token_still_returns_401(self):
        self.start_server()
        status, result = self.post_valid('invalid-synthetic-token')
        self.assertEqual(status, 401)
        self.assertEqual(result, {'error': 'Authentication required'})
        self.assert_empty_database()

    def test_valid_request_after_stalled_body_recovers(self):
        self.start_server()
        client = self.connect_client()
        client.sendall(self.headers(100) + b'{')
        self.assert_timeout_close(client)
        status, result = self.post_valid()
        self.assertEqual(status, 201)
        self.assertIn('request_id', result)


if __name__ == '__main__':
    unittest.main()
