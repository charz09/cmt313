from datetime import datetime
from src import db
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager
from .role import Role

# Included in the other project but no idea what it does yet
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    assessments = db.relationship('Assessment', backref='user', lazy='dynamic')
    questions = db.relationship('Question', backref='user', lazy='dynamic')
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(280))
    login_count = db.Column(db.String)
    

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @staticmethod
    def create(username):  # create new user
        new_user = User(username)
        db.session.add(new_user)
        db.session.commit()

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User %r>' % self.username
