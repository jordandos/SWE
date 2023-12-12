import unittest
from flask import Flask, jsonify
from Website import app, db  # Replace 'Website' with the actual name of your Flask app package

class UsernameLoginTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_valid_usernames(self):
        valid_usernames = ["john_doe123", "alice_789", "user_123"]
        for username in valid_usernames:
            data = {'username': username, 'password': 'test_password'}
            response = self.app.post('/login', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Login successful')
            self.assertEqual(response.json['user_type'], 'student')

    def test_invalid_usernames(self):
        invalid_usernames = ["special@chars", "toolongusername123456", ""]
        for username in invalid_usernames:
            data = {'username': username, 'password': 'test_password'}
            response = self.app.post('/login', json=data)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json['error'], 'Invalid credentials')

    def test_empty_usernames(self):
        data = {'username': '', 'password': 'test_password'}
        response = self.app.post('/login', json=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], 'Invalid credentials')

class ClassRegistrationTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_valid_class_codes(self):
        valid_class_codes = ["CS101", "MATH202", "ENG101"]
        for class_code in valid_class_codes:
            data = {'class_code': class_code}
            response = self.app.post('/register_class', json=data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json['message'], 'Class registration successful')

    def test_invalid_class_codes(self):
        invalid_class_codes = ["INVALID123", "PHY303", "INVALID"]
        for class_code in invalid_class_codes:
            data = {'class_code': class_code}
            response = self.app.post('/register_class', json=data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json['error'], 'Invalid class code')

if __name__ == '__main__':
    unittest.main()
