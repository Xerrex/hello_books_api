"""Test Operations Involving the user model

Operations include: initialisation, Login, Register
"""
from unittest import main
import json

from app import create_app, db
from .my_testbase import TestBase
from app.models import User


class UserModelCase(TestBase):

    def setUp(self):
        self.app = create_app(config_env_name="testing_env")
        self.client = self.app.test_client()

        with self.app.test_request_context():
            db.create_all()

    def tearDown(self):
        self.client.post('/api/v1/auth/logout', content_type='application/json')

        with self.app.test_request_context():
            db.drop_all()

        self.client = None
        self.app = None

    def register_user(self):
        """Register a new user"""
        new_user = {
            "name": "Alex",
            "email": "alex@dev.com",
            "password": "123456789",
            "aboutme": "mad skills you"
        }

        response = self.client.post('/api/v1/auth/register', data=json.dumps(new_user),
                                    content_type='application/json')

        return response

    def login_user(self):
        """Login a user"""

        logins = {
            "email": "alex@dev.com",
            "password": "123456789"
        }

        response = self.client.post('/api/v1/auth/login', data=json.dumps(logins),
                                    content_type='application/json')

        return response

    def test_User_init_is_accurate(self):
        """
        Test that the user model initialisation is accurate
        """
        user = User('Alex', 'alex@dev.com', '12345678', 'dev with mad skills')
        self.assertTrue(user.name == 'Alex')

    def test_user_password_is_hashed(self):
        """
        Test that user password is hashed
        """
        user = User('Alex', 'alex@dev.com', '12345678', 'dev with mad skills')
        user_password_hashed = user.password
        user_password_string = '12345678'

        self.assertFalse(user_password_hashed == user_password_string)
        self.assertTrue(user.verify_password(user_password_string))

    def test_user_registration(self):
        """Test than user can register

        Assert that a valid POST request to /api/v1/auth/register
        registers a new user
        """

        response = self.register_user()

        self.assert201(response)
        self.assertIn("User registration was successful", response.get_data(as_text=True))

    def test_no_duplicate_user_registration(self):
        """Test that user cannot register twice.

        Assert that a valid POST request to /api/v1/auth/register
        fails with error 409 and message in context with the same.
        """
        self.register_user()

        response = self.register_user()

        self.assert409(response)
        self.assertIn('User with that email already exists', response.get_data(as_text=True))

    def test_user_login(self):
        """Test that User can login

        Ensure that a valid POST request to /api/v1/auth/login
        logs in a user.
        """
        self.register_user()

        response = self.login_user()

        data = json.loads(response.get_data(as_text=True))

        self.assert200(response)
        self.assertIn("Alex", data['message'])

    def test_already_logged_in_user(self):
        """Test that user cannot login twice:

        Ensure that a user that is already logged
        cannot log in again.
        """

        self.register_user()

        self.login_user()

        response = self.login_user()
        response_data = json.loads(response.get_data(as_text=True))

        self.assert409(response)

        self.assertIn('Alex', response_data['message'])

    def test_invalid_user_email_login(self):
        """Test that user cannot login if not registered

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
        """Test that user cannot login with wrong password

        Ensure that a valid POST request to /api/v1/auth/login
        with wrong password fails with a 401 status code & message in that context
        """
        self.register_user()

        # login with wrong password that does not exist
        logins = {
            "email": "alex@dev.com",
            "password": "1234567893"
        }

        response = self.client.post('/api/v1/auth/login', data=json.dumps(logins),
                                    content_type='application/json')

        data = json.loads(response.get_data(as_text=True))
        self.assert401(response)
        self.assertIn('password', data['message'])

    def test_User_can_logout(self):
        """Test that User can log out:

        Ensure that valid POST request to /api/v1/auth/logout
        logs out a user.
        """

        self.register_user()

        self.login_user()

        response = self.client.post('/api/v1/auth/logout', content_type='application/json')

        response_data = json.loads(response.get_data(as_text=True))

        self.assert200(response)
        self.assertIn("Alex", response_data["message"])

    def test_only_logged_in_User_logouts(self):
        """Test that user can logout only if logged in

        Ensure that only logged in users can logout
        """

        response = self.client.post('/api/v1/auth/logout', content_type='application/json')

        response_data = json.loads(response.get_data(as_text=True))

        self.assert403(response)
        self.assertIn("Kindly Login first", response_data["message"])

    def test_user_can_reset_password(self):
        """Test that a user can reset their password

        Ensure that a user can be able to reset their password
        """

        # register user
        self.register_user()

        # request password reset token
        new_user_email = {
            'email': "alex@dev.com"
        }
        response = self.client.post('/api/v1/auth/reset-password/request', data=json.dumps(new_user_email),
                                    content_type='application/json')

        # get the reset token
        response_data = json.loads(response.get_data(as_text=True))
        reset_link = response_data['reset_link']

        # make reset with token
        password_reset_request = {
            'email': "alex@dev.com",
            'new_password': '0987654321'
        }

        response = self.client.put(reset_link, data=json.dumps(password_reset_request),
                                    content_type='application/json')

        data = json.loads(response.get_data(as_text=True))

        self.assert200(response)
        self.assertIn('Your password has been successfully reset', data['message'])
        response = self.login_user()
        self.assert401(response)

    def test_only_existing_user_reset_password(self):
        """Test that only existing user can reset password

        Ensure that non existent user cannot reset password.
        """
        # request password reset token
        new_user_email = {
            'email': "alex@dev.com100"
        }
        response = self.client.post('/api/v1/auth/reset-password', data=json.dumps(new_user_email),
                                    content_type='application/json')

        self.assert404(response)


if __name__ == '__main__':
    main(verbosity=2)
