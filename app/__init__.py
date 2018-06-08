from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# local imports
from config import app_env_configs

db = SQLAlchemy()


def create_app(config_env_name):
    app = Flask(__name__)
    app.config.from_object(app_env_configs[config_env_name])

    db.init_app(app)
    Migrate(app, db)

    from .auth import auth_Bp as auth_Blueprint
    app.register_blueprint(auth_Blueprint)

    from .book import book_BP as book_Blueprint
    app.register_blueprint(book_Blueprint)

    from .borrow import borrow_BP as book_Blueprint
    app.register_blueprint(book_Blueprint)

    @app.route('/')
    @app.route('/api/v1/')
    def home():
        return render_template('home.html'), 200

    return app
