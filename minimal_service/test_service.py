import json
import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from minimal_service.service import connect, product, submit, url_parts, work_once


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {'CERBERUS_DB': self.tmp.name + '/research.sqlite'})
        self.env.start()
        self.db = connect()

    def tearDown(self):
        self.db.close()
        self.env.stop()
        self.tmp.cleanup()

    def test_request_worker_and_product(self):
        rid = submit(self.db, {'question': 'Research example', 'sources': ['https://example.org/']})['request_id']
        self.assertTrue(work_once(self.db, lambda url: ('text/plain', b'source passage')))
        eid = self.db.execute('SELECT id FROM evidence').fetchone()['id']
        result = product(self.db, {'request_id': rid, 'text': 'Draft', 'claims': [{'statement': 'Example', 'evidence_ids': [eid]}]})
        self.assertTrue(result['accepted'])
        self.assertFalse(work_once(self.db))

    def test_rejection_is_recorded(self):
        rid = submit(self.db, {'question': 'Research', 'sources': ['https://example.org/']})['request_id']
        result = product(self.db, {'request_id': rid, 'text': 'Draft', 'claims': [{'statement': 'Example', 'evidence_ids': ['missing']}]})
        self.assertFalse(result['accepted'])
        self.assertEqual(self.db.execute('SELECT accepted FROM products').fetchone()[0], 0)

    def test_delete_and_evidence_update_blocked(self):
        submit(self.db, {'question': 'Research', 'sources': ['https://example.org/']})
        work_once(self.db, lambda url: ('text/plain', b'original'))
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('DELETE FROM requests')
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE evidence SET body='replacement'")

    def test_invalid_source_rejected_before_insert(self):
        with self.assertRaises(ValueError):
            submit(self.db, {'question': 'Research', 'sources': ['http://example.org/']})
        self.assertEqual(self.db.execute('SELECT count(*) FROM requests').fetchone()[0], 0)

    def test_duplicate_and_malformed_urls_are_rejected(self):
        with self.assertRaises(ValueError):
            submit(self.db, {'question': 'Research', 'sources': ['https://example.org/', 'https://example.org/']})
        with self.assertRaises(ValueError):
            submit(self.db, {'question': 'Research', 'sources': ['https://example.org/#frag']})

    def test_invalid_claim_shape_is_recorded(self):
        rid = submit(self.db, {'question': 'Research', 'sources': ['https://example.org/']})['request_id']
        result = product(self.db, {'request_id': rid, 'text': 'Draft', 'claims': [{'statement': 'Example'}]})
        self.assertFalse(result['accepted'])
        self.assertIn('Invalid claim structure', result['errors'])

    def test_url_parts_rejects_credentials_and_non_https(self):
        for url in ('http://example.org/', 'https://user@example.org/', 'https://example.org/#fragment'):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    url_parts(url)

    def test_expired_job_is_reclaimed(self):
        rid = submit(self.db, {'question': 'Research', 'sources': ['https://example.org/']})['request_id']
        job_id = self.db.execute('SELECT id FROM jobs WHERE request_id=?', (rid,)).fetchone()['id']
        self.db.execute("UPDATE jobs SET state='running', token='stale', lease_until=0 WHERE id=?", (job_id,))
        self.assertTrue(work_once(self.db, lambda url: ('text/plain', b'fresh evidence')))
        state = self.db.execute('SELECT state FROM jobs WHERE id=?', (job_id,)).fetchone()['state']
        self.assertEqual(state, 'complete')


if __name__ == '__main__':
    unittest.main()
