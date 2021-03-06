# pylint: disable=too-few-public-methods
import os

__all__ = ('config',)


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    # SERVER_NAME = os.getenv('SERVER_NAME', '192.168.0.71:4000')
    SERVER_HEADER = os.getenv('SERVER_HEADER', 'Exim API')
    PREFERRED_URL_SCHEME = os.getenv('PREFERRED_URL_SCHEME', 'https')

    # https://github.com/pallets/flask/issues/2549
    JSONIFY_PRETTYPRINT_REGULAR = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': ProductionConfig 
}

# possible option, exim or postfix
#mailServer = "exim"
mailServer = "postfix"

# exim binary
EXIM = '/usr/sbin/exim'
# postfix sendmail binary
POSTFIX = '/usr/sbin/sendmail'
# dig binary
DIG = '/usr/bin/dig'
