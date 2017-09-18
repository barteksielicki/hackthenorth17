class BaseConfig:
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = ('cockroachdb://hack_user@localhost:26257/hack?'
                               'sslmode=disable')


class DevelopmentConfig(BaseConfig):
    pass


CONFIG_MAPPING = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
}
