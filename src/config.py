import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = '2E[&\xa8\x92\xcffM\x17\x0b\x1a'
    DEBUG = True
    FLASK_ENV = 'development'

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False