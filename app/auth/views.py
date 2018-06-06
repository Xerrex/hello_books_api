from flask import session, url_for
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash, generate_password_hash

from app.data_repo.user_repo import get_user_by_email, create_user, get_user_id, \
    get_user_by_id, password_reset_token, verify_token

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

        self.user_parser.add_argument('aboutme', type=str, location='json')

    def post(self):
        user_args = self.user_parser.parse_args()

        user_name = user_args['name']
        user_email = user_args['email']
        user_password = user_args['password']
        user_aboutme = user_args['aboutme']

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

        user_email = login_args['email']
        user_password = login_args['password']

        user = get_user_by_email(user_email)
        if user and check_password_hash(user['password'], user_password):
            if 'userID' not in session:
                session['userID'] = get_user_id(user_email)
                return {"message": "Welcome back {}".format(user['name'])}, 200
            return {"message": "Your already logged in {}".format(user['name'])}, 409

        return {"message": "Invalid email or password. Makes sure to register first"}, 401


class LogoutResource(Resource):
    logout_parser = reqparse.RequestParser()
    logout_parser.add_argument('userID', type=str, required=True,
                               help="Forbidden Request", location='json')

    def post(self):
        logout_arg = self.logout_parser.parse_args()
        user_id = logout_arg['userID']

        if 'userID' not in session:
            return {"message": "Kindly Login first: Forbidden Action"}, 403

        session.pop('userID', None)

        user_name = get_user_by_id(user_id)['name']

        return {"message": "You have been successfully logged out {}".format(user_name)}, 200


class ResetPassRequestResource(Resource):
    reset_pass_request_parser = reqparse.RequestParser()
    reset_pass_request_parser.add_argument('email', type=email_validator, required=True,
                                   location='json')

    def post(self):
        reset_pass_request_args = self.reset_pass_request_parser.parse_args()
        user_email = reset_pass_request_args['email']

        # generate token just email was passed
        # check if user exists
        if get_user_by_email(user_email):
            # generate token

            response = {
                'message': 'Token generated successfully.Use the token value to reset your password',
                'reset_link': url_for('auth.reset-password', token=password_reset_token(user_email))
            }

            return response, 201

        response = {
            'message': "Your email was Not found. Please register first to reset password"
        }
        return response, 404


class ResetPasswordResource(Resource):
    reset_pass_parser = reqparse.RequestParser()
    reset_pass_parser.add_argument('email', type=email_validator, required=True,
                                           location='json')
    reset_pass_parser.add_argument('new_password', type=length_validator,
                                   required=True, location='json')

    def put(self, token):
        reset_pass_args = self.reset_pass_parser.parse_args()
        user_email = reset_pass_args['email']
        new_password = reset_pass_args['new_password']

        # verify token & reset set password: email, reset_token, new_password are set
        email = verify_token(token)

        if email and email.lstrip('@') == user_email.lstrip('@'):
            # get user
            user = get_user_by_email(user_email)
            user['password'] = generate_password_hash(new_password)
            response = {
                'message': 'Your password has been successfully reset'
            }
            return response, 200

        response = {'message': "Something Went wrong with password reset"}
        return response, 401
