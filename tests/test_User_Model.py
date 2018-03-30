"""
Test Operations Involving the user model
Login , Register too
"""
from unittest import main
import json

from tests import TestBase
from app.models.user import User
from app.views import USERS


class UserModelCase(TestBase):

    user1 = User('Alex','alex@dev.com','12345678','dev with mad skills')

    def test_User_init_is_accurate(self):
        """
        Test that the user model intialisation is accurate
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

        self.assertEqual(response.status_code, 201)
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

        self.assertTrue(response.status_code == 409)
        self.assertIn('User with that email already exists',response.get_data(as_text=True))



if __name__ == '__main__':
    main(verbosity=2)