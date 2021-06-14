"""Routes tested:

"""

from unittest import TestCase
from server import app, session
from model import connect_to_db, create_sample_data
import crud

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


class FlaskTestsLoggedInUser(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                crud.create_sample_data()
                sess['username'] = 'testy'
                sess['password'] = 'test'
                sess['admin'] = False
        
    
    def test_logged_in_homepage(self):
        """Tests user logged in homepage route"""

        res = self.client.get('/')


if __name__ == '__main__':
    import unittest
    connect_to_db(app)
    unittest.main()