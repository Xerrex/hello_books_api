"""
Test Operations Involving the user model
Login, Register
"""
from unittest import main
import json

from tests import TestBase
from app.models.user import User


class UserModelCase(TestBase):
    user1 = User('Alex', 'alex@dev.com', '12345678', 'dev with mad skills')

    def test_User_init_is_accurate(self):
        """
        Test that the user model initialisation is accurate
        """

        self.assertTrue(self.user1.name == 'Alex')

    def test_user_password_is_hashed(self):
        """
        Test that user password is hashed
        """

        user_password_hashed = self.user1.password
        user_password_string = '12345678'

        self.assertFalse(user_password_hashed == user_password_string)
        self.assertTrue(self.user1.verify_password(user_password_string))

    def test_user_registration(self):
        """Test user registration

        Assert that a valid POST request to /api/v1/auth/register
        registers a new user
        """

        new_user = {
            "name": "Alex2",
            "email": "alex@dev.com2",
            "password": "1234567892",
            "aboutme": "mad skills you2"
        }

        response = self.client.post('/api/v1/auth/register', data=json.dumps(new_user),
                                    content_type='application/json')

        self.assert201(response)
        self.assertIn("User registration was successful", response.get_data(as_text=True))

    def test_no_duplicate_user_registration(self):
        """Test no duplicate user registration

        Assert that a valid POST request to /api/v1/auth/register
        fails with error 409 and message in context with the same.
        """

        new_user = {
            "name": "Alex",
            "email": "alex@dev.com",
            "password": "123456789",
            "aboutme": "mad skills you"
        }
        response = self.client.post('/api/v1/auth/register', data=json.dumps(new_user),
                                    content_type='application/json')

        response = self.client.post('/api/v1/auth/register', data=json.dumps(new_user),
                                    content_type='application/json')

        self.assert409(response)
        self.assertIn('User with that email already exists', response.get_data(as_text=True))

    def test_user_login(self):
        """Test User login

        Ensure that a valid POST request to /api/v1/auth/login
        logs in a user.
        """
        new_user = {
            "name": "Alex3",
            "email": "alex@dev.com3",
            "password": "1234567893",
            "aboutme": "mad skills you3"
        }

        response = self.client.post('/api/v1/auth/register', data=json.dumps(new_user),
                                    content_type='application/json')

        logging_credentials = {
            "email": "alex@dev.com3",
            "password": "1234567893"
        }

        response = self.client.post('/api/v1/auth/login', data=json.dumps(logging_credentials),
                                    content_type='application/json')

        response_data = json.loads(response.get_data(as_text=True))

        self.assert200(response)
        self.assertIn(new_user['name'], response_data['message'])

    def test_already_logged_in_user(self):
        """Test that a user cannot login twice:

        Ensure that a user that is already logged
        cannot log in again.
        """

        new_user = {
            "name": "Alex10",
            "email": "alex@dev.com10",
            "password": "12345678910",
            "aboutme": "mad skills you10"
        }

        response = self.client.post('/api/v1/auth/register', data=json.dumps(new_user),
                                    content_type='application/json')

        logging_credentials = {
            "email": "alex@dev.com10",
            "password": "12345678910"
        }

        self.client.post('/api/v1/auth/login', data=json.dumps(logging_credentials),
                                    content_type='application/json')

        response = self.client.post('/api/v1/auth/login', data=json.dumps(logging_credentials),
                                    content_type='application/json')

        response_data = json.loads(response.get_data(as_text=True))

        self.assert409(response)

        self.assertIn('Alex10', response_data['message'])

    def test_invalid_useremail_login(self):
        """Test login with invalid email or email that does not exist

         Ensure that a valid POST request to /api/v1/auth/login
        with wrong email fails with a 401 status code & message in that context
        """
        # login with user that does not exist
        logging_credentials = {
            "email": "alex@dev.com5",
            "password": "1234567893"
        }

        response = self.client.post('/api/v1/auth/login', data=json.dumps(logging_credentials),
                                    content_type='application/json')

        response_data = json.loads(response.get_data(as_text=True))

        self.assert401(response)
        self.assertIn('Invalid email', response_data['message'])

    def test_invalid_password_login(self):
        """Test login with wrong password

        Ensure that a valid POST request to /api/v1/auth/login
        with wrong password fails with a 401 status code & message in that context
        """
        # login with user that does not exist
        logging_credentials = {
            "email": "alex@dev.com30",
            "password": "1234567893"
        }

        response = self.client.post('/api/v1/auth/login', data=json.dumps(logging_credentials),
                                    content_type='application/json')

        response_data = json.loads(response.get_data(as_text=True))

        self.assert401(response)
        self.assertIn('or password. Makes sure to register first', response_data['message'])


if __name__ == '__main__':
    main(verbosity=2)
