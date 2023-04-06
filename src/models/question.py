from src import db
from src.models.assessment import Assessment

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    question_type = db.Column(db.String(30), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    choices = db.relationship('Choice', backref='question', lazy=True)
    correct_count = db.Column(db.Integer, default=0)
    incorrect_count = db.Column(db.Integer, default=0)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)


