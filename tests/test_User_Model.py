"""
Test Operations Involving the user model
Login , Register too
"""
from unittest import main

from tests import TestBase
from app.models.user import User


class UserModelCase(TestBase):

    def setUp(self):
        self.user1 = User('Alex','alex@dev.com','12345678','dev with mad skills')


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

        

if __name__ == '__main__':
    main(verbosity=2)