from datetime import datetime

from flask import session, url_for
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from app.data_repo.user_repo import get_user_by_email, create_user, \
    get_user_by_id, verify_token

from app.utils.data_validators import string_validator, email_validator, length_validator


class RegisterResource(Resource):
    """
    Resource handles user Login
    """

    def __init__(self):
        super().__init__()
        self.user_parser = reqparse.RequestParser()

        self.user_parser.add_argument('name', type=string_validator, required=True,
                                      location='json')

        self.user_parser.add_argument('email', type=email_validator, required=True,
                                      location='json')

        self.user_parser.add_argument('password', type=length_validator, required=True,
                                      location='json')

        self.user_parser.add_argument('about_me', type=str, location='json')

    def post(self):
        user_args = self.user_parser.parse_args()

        user_name = user_args['name']
        user_email = user_args['email']
        user_password = user_args['password']
        user_aboutme = user_args['about_me']

        if get_user_by_email(user_email) is None:

            new_user = create_user(user_name, user_email, user_password, user_aboutme)

            return {
                       "message": "User registration was successful",
                       "details": new_user.__repr__()
                   }, 201
        return {'message': "User with that email already exists"}, 409


class LoginResource(Resource):
    """
    Handle login request
    """

    def __init__(self):
        super().__init__()

        self.login_parser = reqparse.RequestParser()

        self.login_parser.add_argument('email', type=email_validator, required=True,
                                       location='json')

        self.login_parser.add_argument('password', type=length_validator, required=True,
                                       location='json')

    def post(self):
        login_args = self.login_parser.parse_args()

        email = login_args['email']
        password = login_args['password']

        user = get_user_by_email(email)

        if user and user.verify_password(password):
            if 'userID' not in session:
                session['userID'] = user.id

                # update last seen time
                user.last_seen = datetime.utcnow()
                user.save()
                return {
                           "message": "Welcome back {}".format(user.name),
                           "last seen": '{}'.format(user.last_seen)
                       }, 200

            return {
                       "message": "Your already logged in {}".format(user.name),
                       "last seen": '{}'.format(user.last_seen)
                   }, 409
        return {
                   "message": "Invalid email or password. Makes sure to register or reset password",
               }, 401


class LogoutResource(Resource):

    def post(self):

        if 'userID' not in session:
            return {"message": "Kindly Login first: Forbidden Action"}, 403

        user = get_user_by_id(session['userID'])
        session.pop('userID', None)

        return {"message": "You have been successfully logged out {}".format(user.name)}, 200


class ResetPassRequestResource(Resource):
    reset_pass_request_parser = reqparse.RequestParser()
    reset_pass_request_parser.add_argument('email', type=email_validator, required=True,
                                   location='json')

    def post(self):
        reset_pass_request_args = self.reset_pass_request_parser.parse_args()
        user_email = reset_pass_request_args['email']

        # generate token just email was passed
        # check if user exists
        user = get_user_by_email(user_email)
        if user:
            # generate token

            response = {
                'message': 'Token generated successfully.Use the link to reset your password within 5 Minutes',
                'reset_link': url_for('auth.reset-password', token=user.generate_token_value())
            }

            return response, 201

        response = {
            'message': "Your email was Not found. Please register first to reset password"
        }
        return response, 404


class ResetPasswordResource(Resource):
    reset_pass_parser = reqparse.RequestParser()
    reset_pass_parser.add_argument('new_password', type=length_validator,
                                   required=True, location='json')

    def put(self, token):
        reset_pass_args = self.reset_pass_parser.parse_args()
        new_password = reset_pass_args['new_password']

        # verify token
        user = verify_token(token)
        if not user:
            return {'message': "Something Went wrong with the password reset"}, 401

        user.password = generate_password_hash(new_password)
        user.save()
        return {'message': 'Your password has been successfully reset'}, 200
