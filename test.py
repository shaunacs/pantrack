"""Routes tested:
/
/log-in
"""

from unittest import TestCase
from server import app, session
from model import db, connect_to_db, create_sample_data, User
import crud
import os

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
                os.system('dropdb appointments')
                os.system('createdb appointments')
                db.create_all()
                user = crud.create_user('Testing', 'Test', 'testing@test.test', 'testy', 'test', '83838')
                sess['username'] = 'testy'
                sess['password'] = 'test'
                sess['admin'] = False
    
    def tearDown(self):
        """Stuff to do after each test"""

        user = User.query.filter_by(username='test').first()
        db.session.delete(user)
        db.session.commit()
    
    def test_logged_in_homepage(self):
        """Tests user logged in homepage route"""

        res = self.client.post('/log-in',
                                data={"username": "testy", "password": "test"},
                                follow_redirects=True)
        self.assertIn(b'Schedule', res.data)


    # def test_logout(self):
    #     """Tests user log out"""

    #     res = self.client.get('/logout')
    #     self.assertIn(b'log in', res.data)

class FlaskTestsLoggedInAdmin(TestCase):
    """Flask tests with Admin logged in to session"""

    def setUp(self):
        """Stuff to do before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                os.system('dropdb appointments')
                os.system('createdb appointments')
                db.create_all()
                crud.create_admin('Admin', 'Admindy', 'admin@test.test', 'admin', 'test')
                sess['username'] = 'admin'
                sess['password'] = 'test'
                sess['admin'] = True
    

    def test_logged_in_homepage(self):
        """Tests admin logged in homepage route"""

        res = self.client.post('log-in',
                                data={'username': 'admin', 'password': 'test'},
                                follow_redirects=True)
        
        self.assertIn(b'Admin Page', res.data)



if __name__ == '__main__':
    import unittest
    connect_to_db(app)
    unittest.main()