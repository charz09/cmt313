import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ENV = 'development'
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'data/data.sqlite')
