"""Defines methods that manipulate user data.

This methods decouple the views and the models.
"""
from app.models import USERS, User


def create_user(name, email, password, aboutme):
    """ Create a new User
    """
    new_user = User(name, email, password, aboutme)

    user_id = len(USERS) + 1
    user_id = 'user%i' % user_id
    USERS[user_id] = new_user.__dict__

    return new_user


def get_user_by_email(email):
    """ Retrieve a User by email"""

    for user in USERS.values():
        if user['email'] == email:
            return user
    return None


def get_user_id(email):
    """Finds a user id by their email

    :param email:
    """
    for user_id in USERS.keys():
        user_email = USERS[user_id]['email']
        if user_email == email:
            return user_id
    return


def get_user_by_id(user_id):

    return USERS[user_id]


def password_reset_token(email):
    """Generate user Token"""
    token = User.generate_token_value(email)
    return token


def verify_token(token):
    """Check User token"""
    return User.verify_token_value(token)