"""Routes tested:

"""

from unittest import TestCase
from server import app, session
from model import connect_to_db

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def tearDown(self):
        """Stuff to do after each test."""
    

    def test_homepage(self):
        """Test homepage route"""

        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Welcome", res.data)


if __name__ == '__main__':
    import unittest
    connect_to_db(app)
    unittest.main()