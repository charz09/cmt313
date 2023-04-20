from src import db
from .answer import Answer


class Attempt(db.Model):
    __tablename__ = 'attempts'
    id = db.Column(db.Integer, primary_key=True)
    user_score = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    answers = db.relationship('Answer', backref='attempt')

    def __init__(self, assessment_id: int, created_by: int):
        self.assessment_id = assessment_id
        self.created_by = created_by

    @staticmethod
    def create(assessment_id, created_by):  # create new user
        new_attempt = Attempt(assessment_id=assessment_id,
                              created_by=created_by)
        db.session.add(new_attempt)
        db.session.commit()
        return new_attempt

    def __repr__(self):
        return '<Attempt %r>' % self.name
