import os
from _datetime import datetime, timedelta
import jwt

from werkzeug.security import generate_password_hash, check_password_hash


class User(object):
    """class defines User data model

    name, email, password, aboutme, lastseen
    """
    def __init__(self, name=None, email=None, password=None, aboutme=None):
        self.name = name
        self.email = email  # Email should be unique
        self.password = generate_password_hash(password)
        self.aboume = aboutme
        self.lastseen = datetime.utcnow()

    def verify_password(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return check_password_hash(self.password, password)

    def __repr__(self):
        """
        Defines how to print the User model
        """
        return 'User-{}-{}-{}'.format(self.name, self.email, self.lastseen)

    @staticmethod
    def generate_token_value(user_email):
        """Generate JSON WEB TOKEN based on the user's email

        :param user_email:
        :return jwt_token:
        """
        user_email = user_email.lstrip('@')
        secret = os.environ.get('SECRET_KEY') or 'prepare to be amazed'

        payload = {
            'reset_password_email': user_email,
            'exp': datetime.utcnow() + timedelta(minutes=5),
            'iat': datetime.utcnow()
        }

        jwt_token = jwt.encode(payload, secret, algorithm='HS256').decode('utf-8')

        return jwt_token

    @staticmethod
    def verify_token_value(token):
        """Verify JSON WEB TOKEN value

        :param token:
        :return user's email:
        """
        secret = os.environ.get('SECRET_KEY') or 'prepare to be amazed'
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            email = payload['reset_password_email']
            return email
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
