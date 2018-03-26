from flask import Flask
from flask_restful import Api

#local imports
from config import app_env_configs


def create_app(config_env_name):
    app = Flask(__name__)
    app.config.from_object(app_env_configs[config_env_name])

    api = Api(app)

    #import Resources
    from app.views import BookResource


    #register endpoint
    api.add_resource(BookResource, '/api/books')

    return app
