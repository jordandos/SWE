import unittest
from flask import Flask, jsonify
from Website import app, db  # Replace 'Website' with the actual name of your Flask app package

class UsernameRulesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_registration_success(self):
        data = {'username': 'test_user', 'password': 'test_password', 'user_type': 'student'}
        response = self.app.post('/register', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], 'Registration successful')

    def test_registration_username_taken(self):
        # Register a user first
        data = {'username': 'existing_user', 'password': 'password', 'user_type': 'student'}
        self.app.post('/register', json=data)

        # Try to register another user with the same username
        data = {'username': 'existing_user', 'password': 'another_password', 'user_type': 'student'}
        response = self.app.post('/register', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Username is already taken')

class ClassRegistrationRulesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    # Add more test cases related to class registration rules here

if __name__ == '__main__':
    unittest.main()
