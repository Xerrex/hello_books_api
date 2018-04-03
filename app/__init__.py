from flask import Flask
from flask_restful import Api

# local imports
from config import app_env_configs


def create_app(config_env_name):
    app = Flask(__name__)
    app.config.from_object(app_env_configs[config_env_name])

    api = Api(app)

    # import Resources
    from app.views import BookListResource, BookResource, UserRegisterResource, \
        UserLoginResource, UserLogoutResource, UserResetPasswordResource, BorrowResource


    # register endpoint

    api.add_resource(BookListResource, '/api/v1/books', endpoint="lists")
    api.add_resource(BookResource, '/api/v1/books/<bookId>', endpoint="list")

    api.add_resource(UserRegisterResource, '/api/v1/auth/register', endpoint="register")
    api.add_resource(UserLoginResource, '/api/v1/auth/login', endpoint="login")
    api.add_resource(UserLogoutResource, '/api/v1/auth/logout', endpoint='logout')
    api.add_resource(UserResetPasswordResource, '/api/v1/auth/reset-password', endpoint='reset-password')

    api.add_resource(BorrowResource, '/api/v1/users/books/<bookId>', endpoint='borrow')

    return app
