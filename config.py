import os


class Config(object):
    """Parent configuration class for enviroments.
    """

    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'prepare to be amazed'


class Development_env(Config):
    """
    Development enviroment configurations
    """
    DEBUG = True


class Testing_env(Config):
    """
    Testing enviroment configurations
    """
    DEBUG = True
    TESTING = True


class Production_env(Config):
    """
    Production enviroment configurations
    """

    DEBUG = False


app_env_configs = {
    'dev_env': Development_env,
    'pro_env': Production_env,
    'testing_env': Testing_env
}
