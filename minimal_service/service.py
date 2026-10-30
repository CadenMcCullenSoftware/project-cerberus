"""Local research API and worker. Standard library only; not a production service."""
import hashlib
import hmac
import http.client
import ipaddress
import json
import os
import socket
import sqlite3
import ssl
import sys
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

LIMIT = 262144

def now():
    return datetime.now(timezone.utc).isoformat()

def connect():
    path = Path(os.environ['CERBERUS_DB'])
    if not path.is_absolute():
        raise ValueError('CERBERUS_DB must be an absolute path outside the repository')
    root = Path(__file__).resolve().parents[1]
    resolved = path.resolve()
    if resolved == root or root in resolved.parents:
        raise ValueError('Database must be outside the repository')
    db = sqlite3.connect(path, timeout=10, isolation_level=None)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    db.execute('PRAGMA journal_mode=WAL')
    db.executescript('''
    CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY, question TEXT NOT NULL, created_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY, request_id TEXT NOT NULL REFERENCES requests(id), url TEXT NOT NULL, state TEXT NOT NULL, lease_until REAL NOT NULL DEFAULT 0, token TEXT, error TEXT);
    CREATE TABLE IF NOT EXISTS evidence(id TEXT PRIMARY KEY, job_id TEXT NOT NULL UNIQUE REFERENCES jobs(id), request_id TEXT NOT NULL REFERENCES requests(id), url TEXT NOT NULL, fetched_at TEXT NOT NULL, sha256 TEXT NOT NULL, media_type TEXT NOT NULL, body BLOB NOT NULL);
    CREATE TABLE IF NOT EXISTS products(id TEXT PRIMARY KEY, request_id TEXT NOT NULL REFERENCES requests(id), created_at TEXT NOT NULL, content TEXT NOT NULL, accepted INTEGER NOT NULL, errors TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY, created_at TEXT NOT NULL, kind TEXT NOT NULL, payload TEXT NOT NULL);
    ''')
    for table in ('requests', 'jobs', 'evidence', 'products', 'events'):
        db.execute(f"CREATE TRIGGER IF NOT EXISTS {table}_no_delete BEFORE DELETE ON {table} BEGIN SELECT RAISE(ABORT, 'deletion disabled'); END")
    for table in ('requests', 'evidence', 'products', 'events'):
        db.execute(f"CREATE TRIGGER IF NOT EXISTS {table}_no_update BEFORE UPDATE ON {table} BEGIN SELECT RAISE(ABORT, 'immutable record'); END")
    return db

def event(db, kind, payload):
    db.execute('INSERT INTO events VALUES(?,?,?,?)', (uuid.uuid4().hex, now(), kind, json.dumps(payload)))

def url_parts(url):
    if type(url) is not str or len(url) > 2048:
        raise ValueError('Invalid source URL')
    p = urlsplit(url)
    if p.scheme != 'https' or not p.hostname or p.username is not None or p.password is not None or p.port not in (None, 443) or p.fragment:
        raise ValueError('Only HTTPS port 443 URLs without credentials or fragments are accepted')
    return p

def fetch(url):
    p = url_parts(url)
    host = p.hostname.encode('idna').decode('ascii')
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise ValueError('Source must resolve exclusively to public addresses')
    address = addresses[0][4][0]
    conn = http.client.HTTPSConnection(host, timeout=10)
    raw = socket.create_connection((address, 443), timeout=10)
    try:
        conn.sock = ssl.create_default_context().wrap_socket(raw, server_hostname=host)
        conn.request('GET', p.path + ('?' + p.query if p.query else '') or '/', headers={'User-Agent': 'CERBERUS-research/0.1', 'Accept-Encoding': 'identity'})
        response = conn.getresponse()
        if response.status != 200:
            raise ValueError('Source did not return HTTP 200; redirects are not followed')
        if response.getheader('Content-Encoding', 'identity').lower() != 'identity':
            raise ValueError('Encoded responses are unsupported')
        media = response.getheader('Content-Type', '').split(';')[0].lower().strip()
        if media not in ('text/plain', 'text/html', 'application/json'):
            raise ValueError('Unsupported source media type')
        body = response.read(LIMIT + 1)
        if not body or len(body) > LIMIT:
            raise ValueError('Source is empty or exceeds the byte limit')
        return media, body
    finally:
        conn.close()
        raw.close()

def submit(db, data):
    if type(data) is not dict or set(data) != {'question', 'sources'}:
        raise ValueError('Expected question and sources only')
    question, sources = data['question'], data['sources']
    if type(question) is not str or not question.strip() or len(question) > 10000 or type(sources) is not list or not 1 <= len(sources) <= 10:
        raise ValueError('Nonblank question and 1 to 10 source URLs required')
    for source in sources:
        url_parts(source)
    if len(set(sources)) != len(sources):
        raise ValueError('Duplicate sources')
    key = uuid.uuid4().hex
    db.execute('BEGIN IMMEDIATE')
    try:
        db.execute('INSERT INTO requests VALUES(?,?,?)', (key, question, now()))
        for source in sources:
            db.execute('INSERT INTO jobs(id,request_id,url,state) VALUES(?,?,?,?)', (uuid.uuid4().hex, key, source, 'pending'))
        event(db, 'request_accepted', {'request_id': key})
        db.execute('COMMIT')
    except Exception:
        db.execute('ROLLBACK')
        raise
    return {'request_id': key}

def product(db, data):
    if type(data) is not dict or set(data) != {'request_id', 'text', 'claims'}:
        raise ValueError('Expected request_id, text and claims only')
    rid = data['request_id']
    if type(rid) is not str or not db.execute('SELECT 1 FROM requests WHERE id=?', (rid,)).fetchone():
        raise ValueError('Unknown request')
    errors = []
    if type(data['text']) is not str or not data['text'].strip():
        errors.append('Nonblank text required')
    claims = data['claims']
    if type(claims) is not list or not claims:
        errors.append('At least one sourced claim required')
    else:
        for claim in claims:
            if type(claim) is not dict or set(claim) != {'statement', 'evidence_ids'} or type(claim.get('statement')) is not str or not claim['statement'].strip() or type(claim.get('evidence_ids')) is not list or not claim['evidence_ids']:
                errors.append('Invalid claim structure')
                continue
            for eid in claim['evidence_ids']:
                if type(eid) is not str or not db.execute('SELECT 1 FROM evidence WHERE id=? AND request_id=?', (eid, rid)).fetchone():
                    errors.append('Unknown or cross-request evidence')
    key = uuid.uuid4().hex
    db.execute('BEGIN IMMEDIATE')
    try:
        db.execute('INSERT INTO products VALUES(?,?,?,?,?,?)', (key, rid, now(), json.dumps(data), int(not errors), json.dumps(errors)))
        event(db, 'product_accepted' if not errors else 'product_rejected', {'product_id': key, 'request_id': rid, 'errors': errors})
        db.execute('COMMIT')
    except Exception:
        db.execute('ROLLBACK')
        raise
    return {'product_id': key, 'accepted': not errors, 'errors': errors}

def work_once(db, fetcher=fetch):
    token = uuid.uuid4().hex
    db.execute('BEGIN IMMEDIATE')
    try:
        job = db.execute("SELECT * FROM jobs WHERE state='pending' OR (state='running' AND lease_until<?) ORDER BY rowid LIMIT 1", (time.time(),)).fetchone()
        if not job:
            db.execute('COMMIT')
            return False
        db.execute("UPDATE jobs SET state='running',token=?,lease_until=? WHERE id=?", (token, time.time() + 120, job['id']))
        event(db, 'job_claimed', {'job_id': job['id']})
        db.execute('COMMIT')
    except Exception:
        db.execute('ROLLBACK')
        raise
    try:
        media, body = fetcher(job['url'])
        error = None
    except Exception as exc:
        media, body, error = None, None, type(exc).__name__
    db.execute('BEGIN IMMEDIATE')
    try:
        current = db.execute('SELECT token FROM jobs WHERE id=?', (job['id'],)).fetchone()
        if current['token'] == token:
            if error is None:
                db.execute('INSERT INTO evidence VALUES(?,?,?,?,?,?,?,?)', (uuid.uuid4().hex, job['id'], job['request_id'], job['url'], now(), hashlib.sha256(body).hexdigest(), media, body))
            db.execute('UPDATE jobs SET state=?,error=?,lease_until=0 WHERE id=?', ('failed' if error else 'complete', error, job['id']))
            event(db, 'evidence_failed' if error else 'evidence_recorded', {'job_id': job['id'], 'error': error})
        db.execute('COMMIT')
    except Exception:
        db.execute('ROLLBACK')
        raise
    return True

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def respond(self, code, result):
        body = json.dumps(result).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def handle_request(self):
        expected = 'Bearer ' + os.environ['CERBERUS_TOKEN']
        if not hmac.compare_digest(self.headers.get('Authorization', '').encode(), expected.encode()):
            return self.respond(401, {'error': 'Authentication required'})
        if self.command == 'DELETE':
            return self.respond(405, {'error': 'Deletion is disabled'})
        db = connect()
        try:
            if self.command == 'POST' and self.path in ('/requests', '/products'):
                if self.headers.get('Transfer-Encoding') or self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
                    raise ValueError('JSON with Content-Length required')
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= LIMIT:
                    raise ValueError('Invalid request size')
                data = json.loads(self.rfile.read(size))
                result = submit(db, data) if self.path == '/requests' else product(db, data)
                return self.respond(422 if result.get('accepted') is False else 201, result)
            if self.command == 'GET' and self.path.startswith('/requests/'):
                rid = self.path.removeprefix('/requests/')
                row = db.execute('SELECT * FROM requests WHERE id=?', (rid,)).fetchone()
                if not row:
                    return self.respond(404, {'error': 'Unknown request'})
                result = dict(row)
                result['jobs'] = [dict(r) for r in db.execute('SELECT id,url,state,error FROM jobs WHERE request_id=?', (rid,))]
                result['evidence'] = [dict(r) for r in db.execute('SELECT id,url,fetched_at,sha256,media_type FROM evidence WHERE request_id=?', (rid,))]
                return self.respond(200, result)
            self.respond(404, {'error': 'Unknown endpoint'})
        except (ValueError, TypeError, OverflowError, RecursionError):
            self.respond(400, {'error': 'Invalid request'})
        except Exception:
            self.respond(500, {'error': 'Internal failure; no approval inferred'})
        finally:
            db.close()

    do_GET = do_POST = do_DELETE = handle_request

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ('server', 'worker'):
        raise SystemExit('Usage: service.py server|worker')
    if sys.argv[1] == 'server':
        if len(os.environ.get('CERBERUS_TOKEN', '')) < 32:
            raise SystemExit('Set a CERBERUS_TOKEN of at least 32 characters')
        check = connect()
        check.close()
        HTTPServer.allow_reuse_address = False
        HTTPServer(('127.0.0.1', 8765), Handler).serve_forever()
    else:
        db = connect()
        try:
            while True:
                if not work_once(db):
                    time.sleep(1)
        finally:
            db.close()
