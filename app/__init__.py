from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# local imports
from config import env_configs

db = SQLAlchemy()


def create_app(config_env):
    app = Flask(__name__)
    app.config.from_object(env_configs[config_env])

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
