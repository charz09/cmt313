from datetime import datetime

from sqlalchemy import ForeignKeyConstraint, ForeignKey, Column, Integer, String
# from .attempt import attempt
from src.models import attempt
# from src.models.assessment_factory import create_assessment
# from flask_sqlalchemy import SQLAlchemy
from src import db

# db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    teacher_seen = db.Column(db.Boolean, default=False)
    student = db.relationship('Student', backref='feedback')
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempt.id'))
    attempt = db.relationship('Attempts', backref='feedback', lazy=True)
    ################################
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    assessment = db.relationship('Assessment', backref='feedbacks')
    


class Attempts(db.Model):
    __tablename__ = 'attempt'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    score = db.Column(db.Float)
    student = db.relationship('Student', backref='attempt')
    quiz = db.relationship('Quiz', backref='attempt')

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

db.create_all()
