"""Test data validators

"""
from unittest import TestCase

from app.utils.data_validators import email_validator, length_validator


class ValidatorsCase(TestCase):

    def test_email_validator(self):
        """ Test Email Validation

        This test cover both the string & Email validators
        """

        value = "alex@dev.com"
        self.assertEqual(email_validator(value), value)

        value = ""
        self.assertRaises(ValueError, email_validator, value)
        self.assertRaisesRegex(ValueError, 'email value cannot be empty', email_validator, value)

        value = "       "
        self.assertRaisesRegex(ValueError, 'email value cannot contain spaces or tabs only',
                               email_validator, value)

        value = "alexdev.com"
        self.assertRaisesRegex(ValueError, "Invalid email address. Must have '@' ",
                               email_validator, value)

        value = "3alex@dev.com"
        self.assertRaisesRegex(ValueError, "Invalid email address: Cannot start with digit",
                               email_validator, value)

    def test_length_validator(self):
        """Test Length validator"""

        value = " "
        self.assertRaises(ValueError, length_validator, value, 'password', 8)

        value = "12345"
        self.assertRaisesRegex(ValueError, "password must contain not less that 8 characters",
                               length_validator, value, 'password', 8)
        value = "123456789"
        self.assertEquals(length_validator(value, name="Password"), value)
