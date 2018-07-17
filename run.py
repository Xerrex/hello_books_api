import os

config_env= os.getenv('FLASK_CONFIG') or 'pro'

from app import create_app

app = create_app(config_env)

if __name__ == '__main__':
    app.run()