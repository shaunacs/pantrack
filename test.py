"""Routes tested:
/
/log-in
/logout
/create-account
/household-info
"""

from unittest import TestCase
from server import app, session
from model import (db, connect_to_db, create_sample_data, User,
                    Admin, Household)
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
    

    def test_household_rendering(self):
        """Test rendering of household form"""

        res = self.client.get('/household-info')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Household Info", res.data)
    

    def test_create_account(self):
        """Test create account route renders create account page"""

        res = self.client.get('/create-account')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Create an account', res.data)


    def test_handle_create_account(self):
        """Tests that submitting create account form creates a user"""

        create_account_data = {'fname': 'Create',
                                'lname': 'Account',
                                'email': 'create@test.test',
                                'username': 'create',
                                'password': 'test',
                                'phone-number': '44444'}
        
        res = self.client.post('/handle-create-account',
                                data=create_account_data,
                                follow_redirects=True)
        self.assertEqual(User.query.all()[-1], User.query.filter_by(username='create').first())

class FlaskTestsLoggedInUser(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:

                user = crud.create_user('Testy', 'Tester', 'test@test.test', 'testuser', 'test', '5555')
                sess['username'] = 'testuser'
                sess['password'] = 'test'
                sess['admin'] = False
    
    def tearDown(self):
        """Stuff to do after each test"""

        user = User.query.filter_by(username='testuser').first()
        db.session.delete(user)
        db.session.commit()
    
    def test_logged_in_homepage(self):
        """Tests user logged in homepage route"""

        res = self.client.post('/log-in',
                                data={"username": "testuser", "password": "test"},
                                follow_redirects=True)
        self.assertIn(b'Schedule', res.data)


    def test_logout(self):
        """Tests user log out"""

        res = self.client.get('/logout',
                                data={"username": "testuser", "password": "test"},
                                follow_redirects=True)
        self.assertIn(b'log in', res.data)


    def test_handle_household(self):
        """Test creation of user household"""

        user = User.query.first()

        create_household_data = {'num-people': 3,
                                'wants-peanut-butter': 'False',
                                'picking-up-for-another': 'False',
                                'allergies': 'peanuts',
                                'special-requests': ''}
        
        res = self.client.post('/handle-household-info',
                                data=create_household_data,
                                follow_redirects=True)
        self.assertIn(b'Schedule Appointment', res.data)



class FlaskTestsLoggedInAdmin(TestCase):
    """Flask tests with Admin logged in to session"""

    def setUp(self):
        """Stuff to do before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                # os.system('dropdb testdb')
                # os.system('createdb testdb')
                # connect_to_db(app, "postgresql:///testdb")

                # db.create_all()
                crud.create_admin('Admin', 'Admindy', 'admin@test.test', 'admin', 'test')
                sess['username'] = 'admin'
                sess['password'] = 'test'
                sess['admin'] = True
    
    def tearDown(self):
        """Stuff to do after each test"""

        admin = Admin.query.filter_by(username='admin').first()
        db.session.delete(admin)
        db.session.commit()
    

    def test_logged_in_homepage(self):
        """Tests admin logged in homepage route"""

        res = self.client.post('log-in',
                                data={'username': 'admin', 'password': 'test'},
                                follow_redirects=True)
        
        self.assertIn(b'Admin Page', res.data)
    

    def test_logout(self):
        """Tests admin log out"""

        res = self.client.get('/logout',
                                data={'username': 'admin', 'password': 'test'},
                                follow_redirects=True)
        self.assertIn(b'log in', res.data)



if __name__ == '__main__':
    import unittest
    os.system('dropdb testdb')
    os.system('createdb testdb')
    connect_to_db(app, "postgresql:///testdb")
    db.create_all()
    unittest.main()