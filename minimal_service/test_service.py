import json
import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from minimal_service.service import connect, product, submit, work_once

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

if __name__ == '__main__':
    unittest.main()
