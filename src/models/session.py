from src import db
from..models.user import User
import datetime

class UserSession(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.DateTime, server_default=db.func.now())
    end_time = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    
    def __init__(self, user_id, login_count=0):
        self.user_id = user_id
        self.login_count = login_count