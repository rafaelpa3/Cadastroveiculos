class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class Developer(Config):
    MODE = "DEVELOPER"
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

class Production(Config):
    MODE = "PRODUCTION"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'