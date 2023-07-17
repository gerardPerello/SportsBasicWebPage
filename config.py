from decouple import config
class Config:
    pass

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='localhost')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = "/static"
    TEMPLATE_FOLDER = "/templates"
    SECRET_KEY = config('SECRET_KEY', default='localhost')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://lwvmbyftfknsrj:e6d47aecb3ce18bedeb2e88079cc55d936e490e8a3ee942b11fb6418d16cc30e@ec2-34-231-221-151.compute-1.amazonaws.com:5432/daruinjc5e24bh'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = "/frontend/dist/static"
    TEMPLATE_FOLDER = "/frontend/dist"
    SECRET_KEY = "1q2s3f5g7jggujbffrhnbcdgh78jbhd"

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

