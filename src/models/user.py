
from src import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager
from .role import Role
from .module import Module

user_module = db.Table('user_module',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('users.id')),
                       db.Column('module_id', db.Integer,
                                 db.ForeignKey('modules.id'))
                       )


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # assessments = db.relationship('Assessment', backref='user', lazy='dynamic')
    questions = db.relationship('Question', backref='user', lazy='dynamic')
    answers = db.relationship('Answer', backref='user', lazy='dynamic')
    attempts = db.relationship('Attempt', backref='user')
    modules = db.relationship('Module', secondary='user_module')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username: str, password: str, role_id: str):
        self.username = username
        self.password = password
        self.role_id = role_id

    @staticmethod
    def create(username, password, role):  # create new user
        new_user = User(username, password, role)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def __repr__(self):
        return '<User %r>' % self.username
