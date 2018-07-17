import os


class Config(object):
    """Parent configuration class for enviroments.
    """

    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'prepare to be amazed'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentEnv(Config):
    """
    Development enviroment configurations
    """
    DEBUG = True


class TestingEnv(Config):
    """
    Testing enviroment configurations
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_TEST')


class ProductionEnv(Config):
    """
    Production enviroment configurations
    """

    DEBUG = False


env_configs = {
    'dev': DevelopmentEnv,
    'pro': ProductionEnv,
    'testing': TestingEnv
}
