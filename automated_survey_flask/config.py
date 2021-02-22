import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


class DevelopmentConfig(DefaultConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URI')
        or f"sqlite:///{os.path.join(basedir, 'dev.sqlite')}"
    )
    DEBUG = True


class TestConfig(DefaultConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SERVER_NAME = 'server.test'
    TESTING = True
    DEBUG = True


config_env_files = {
    'testing': 'automated_survey_flask.config.TestConfig',
    'development': 'automated_survey_flask.config.DevelopmentConfig',
    'production': 'automated_survey_flask.config.DefaultConfig',
}
