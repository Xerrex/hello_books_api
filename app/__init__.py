from flask import Flask

# local imports
from config import app_env_configs


def create_app(config_env_name):
    app = Flask(__name__)
    app.config.from_object(app_env_configs[config_env_name])

    from .auth import auth_Bp as auth_Blueprint
    app.register_blueprint(auth_Blueprint)

    from .book import book_BP as book_Blueprint
    app.register_blueprint(book_Blueprint)

    from .borrow import borrow_BP as book_Blueprint
    app.register_blueprint(book_Blueprint)

    return app
