import os


class Config(object):
    """Main Config class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Development Configurations inherited from Config."""
    DEBUG = True


class TestingConfig(Config):
    """Testing Configurations inherited from Config"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True


class StagingConfig(Config):
    """Staging Configurations inherited from Config."""
    DEBUG = True


class ProductionConfig(Config):
    """Production Configurations inherited from Config."""
    DEBUG = True
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
