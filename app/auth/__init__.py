from flask import Blueprint
from flask_restful import Api

from .views import RegisterResource, LoginResource, \
    LogoutResource, ResetPassRequestResource, ResetPasswordResource

auth_Bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

api = Api(auth_Bp)

api.add_resource(RegisterResource, '/register', endpoint="register")

api.add_resource(LoginResource, '/login', endpoint="login")

api.add_resource(LogoutResource, '/logout', endpoint='logout')

api.add_resource(ResetPassRequestResource, '/reset-password-request',
                 endpoint='reset-request')

api.add_resource(ResetPasswordResource, '/reset-password/<token>',
                 endpoint='reset-password')
