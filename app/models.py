import os
from _datetime import datetime, timedelta
import jwt

from werkzeug.security import generate_password_hash, check_password_hash
from app import db

USERS = {}  # stores User models

BOOKS = {}  # stores Book models

BORROWS = {}  # stores Borrow models


class User(db.Model):
    """class defines User data model

    name, email, password, about_me, last_seen, is_admin
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    about_me = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password, about_me):
        """Initialise a new instance of User class

         :param name:
         :param email:
         :param password:
         :param about_me:
         """
        self.name = name
        self.email = email  # Email should be unique
        self.password = generate_password_hash(password)
        self.about_me = about_me
        self.last_seen = datetime.utcnow()

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def verify_password(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return check_password_hash(self.password, password)

    def __repr__(self):
        """
        Defines how to print the User model
        """
        return 'User-{}-{}-{}'.format(self.name, self.email, self.last_seen)

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


class Section(db.Model):
    """This Defines the Section Data model

    id, name
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    books = db.relationship('Book', backref='section', lazy=True)

    def __init__(self, name):
        """Creates a new Section Instance

        :param name
        """
        self.name = name

    def save(self):
        """Save a section to the database.
        This includes creating a new cook section and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """Define how the Section is represented"""

        return 'section-{}'.format(self.name)


class Book(db.Model):
    """This defines the Book data model

    name, description, section, quantity
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'),
                        nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def __init__(self, name, description, section, quantity):
        """creates a new Book instance

        :param name:
        :param description:
        :param section:
        :param quantity:
        """
        self.name = name
        self.description = description
        self.section_id = section
        self.quantity = quantity

    def save(self):
        """Save a book to the database.
        This includes creating a new book and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """
        Defines how to print the book  model
        """

        return 'Book:{}-{}'.format(self.name, self.quantity)


class Borrow(db.Model):
    """Borrow model

    This class defines the borrowing of a book by a user
    user_id, book_id, borrowed_at, due_at, is_returned
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self,user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id
        self.borrowed_at = datetime.utcnow()
        self.due_at = datetime.utcnow() + timedelta(days=3)
        self.is_active = True

    def save(self):
        """Save a Borrow to the database.
        This includes borrowing a book and returning one.
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """Define how Borrow is represented
        """
        return 'borrowed-{}-{}-{}'.format(self.book_id,
                                          self.borrowed_at,
                                          self.is_active)



