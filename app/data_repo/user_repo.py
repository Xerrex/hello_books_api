"""Defines methods that manipulate user data.

This methods decouple the views and the models.
"""
from app.models import USERS, User


def create_user(name, email, password, about_me):
    """ Create a new User
    """
    new_user = User(name, email, password, about_me)

    new_user.save()

    return new_user


def get_user_by_email(email):
    """ Retrieve a User by email"""

    user = User.query.filter_by(email=email).first()

    if user:
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

    return User.query.get(user_id)


def verify_token(token):
    """Check User token"""
    return User.verify_token_value(token)