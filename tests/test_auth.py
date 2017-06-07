import sys
import unittest
import json

from os import path
from app import create_app, db

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class AuthTestCase(unittest.TestCase):
    """Test for successful authentication"""

    def setUp(self):
        """Sample user data"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {
            'email': 'sharon@sharon.com',
            'password': 'sharon'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_register_password_length(self):
        """Test that register accepts only the recommended password length"""
        response = self.client().post("/api/v1.0/auth/register",
                                      data={'email': 'sharon@gmail.com',
                                            'password': 'sha'})
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            "The length of the password should be at least six characters")
        self.assertEqual(response.status_code, 411)

    def test_register_email_format(self):
        """Test that register uses right email format"""
        response = self.client().post("/api/v1.0/auth/register",
                                      data={'email': 'sharonsyra',
                                            'password': 'sharon'})
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], "Use the correct email format")
        self.assertEqual(response.status_code, 400)

    def test_registration(self):
        """Test that a user can be registered."""
        response = self.client().post('/api/v1.0/auth/register',
                                      data=self.user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], "You registered successfully. Login.")
        self.assertEqual(response.status_code, 201)

    def test_register_duplicates(self):
        """Test that user is registered only once"""
        response = self.client().post('/api/v1.0/auth/register',
                                      data=self.user_data)
        self.assertEqual(response.status_code, 201)
        second_response = self.client().post(
            '/api/v1.0/auth/register', data=self.user_data)
        self.assertEqual(second_response.status_code, 409)
        result = json.loads(second_response.data.decode())
        self.assertEqual(
            result['message'], "User already exists. Login.")

    def test_login_blank_credential(self):
        """Test that login rejects blank username or password"""
        response = self.client().post('/api/v1.0/auth/login',
                                      data={'email': '', 'password': ''})
        self.assertEqual(response.status_code, 401)

    def test_user_login(self):
        """Test that registered users can login."""
        response = self.client().post('/api/v1.0/auth/register',
                                      data=self.user_data)
        self.assertEqual(response.status_code, 201)
        login_response = self.client().post('/api/v1.0/auth/login',
                                            data=self.user_data)
        result = json.loads(login_response.data.decode())
        self.assertEqual(result['message'], "You logged in successfully.")
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_non_registered_user_login(self):
        """Test that non registered users cannot login."""
        unauthorized_personel = {
            'email': 'sharon@gmail.com',
            'password': 'gmail'
        }
        response = self.client().post('/api/v1.0/auth/login',
                                      data=unauthorized_personel)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again.")
