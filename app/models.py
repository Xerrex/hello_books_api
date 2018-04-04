import os
from _datetime import datetime, timedelta
import jwt

from werkzeug.security import generate_password_hash, check_password_hash

from flask_restful import abort

USERS = {}  # stores User models

BOOKS = {}  # stores Book models

BORROWS = {}  # stores Borrow models


def get_user_id(email):
    """Finds a user by their email

    :param email:
    """
    for user_id in USERS.keys():
        user_email = USERS[user_id]['email']
        if user_email == email:
            return user_id
    return


def abort_if_book_does_not_exist(book_id):
    if book_id not in BOOKS:
        abort(404, message="Book:{} doesn't exist".format(book_id))


def abort_if_same_book_already_borrowed(user_id, book_id):

    """
    Abort when a user has already borrowed the same book
    """

    for borrow in BORROWS.values():
        if borrow['user_id'] == user_id and borrow['book_id'] == book_id:
            if borrow['is_active'] is True:
                abort(409, message="You already have the book borrowed")
    return None


class User(object):
    """class defines User data model

    name, email, password, aboutme, lastseen
    """

    def __init__(self, name=None, email=None, password=None, aboutme=None):
        """Initialise a new instance of User class

         :param name:
         :param email:
         :param password:
         :param aboutme:
         """
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
        :return user's email without the '@':
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


class Book(object):
    """This defines the Book data model

    name, description, section, quantity
    """
    def __init__(self, name, description, section, quantity):
        """creates a new Book instance

        :param name:
        :param description:
        :param section:
        :param quantity:
        """
        self.name = name
        self.description = description
        self.section = section
        self.quantity = int(quantity)

    def __repr__(self):
        """
        Defines how to print the book  model
        """

        return 'Book:{}-{}'.format(self.name, self.quantity)


class Borrow(object):
    """Borrow model

    This class defines the borrowing of a book by a user
    user_id, book_id, borrowed_at, due_at, is_returned
    """
    def __init__(self,user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id
        self.borrowed_at = datetime.utcnow()
        self.due_at = datetime.utcnow() + timedelta(days=3)
        self.is_active = True

    def __repr__(self):
        """Define how Borrow is represented
        """
        return 'borrowed-{}-{}-{}'.format(self.book_id,
                                          self.borrowed_at,
                                          self.is_active)