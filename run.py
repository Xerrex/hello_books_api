import os

config_env_name = os.getenv('FLASK_CONFIG')

from app import create_app

app = create_app(config_env_name)

if __name__ == '__main__':
    app.run()