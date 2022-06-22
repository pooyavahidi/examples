import unittest
import json
from api.app import app

class TestRoot(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.resource_path = "/"
    def tearDown(self):
        return super().tearDown()

    def test_get(self):
        r = self.client.get(self.resource_path)
        resp = json.loads(r.data)
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(resp['receivedAt'])
        self.assertIsNotNone(resp['localIp'])

    def test_get_health(self):
        r = self.client.get(self.resource_path + 'health')
        self.assertEqual(b'healthy', r.data)
