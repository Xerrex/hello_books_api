from _datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(object):
    """class defines User data model

    name, email, password, aboutme, lastseen
    """
    def __init__(self, name, email, password, aboutme=None):
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
