
class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = '7fa1623ffbd1fa466d2f55ab2effccbbbd3fdbc6fee64e2e'
    SQLALCHEMY_DATABASE_URI = "postgresql://form_api_usr:JUGhj6Nhj876mjvFSD@localhost/form_api_db"


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

CURRENT_CONFIG = 'development'
