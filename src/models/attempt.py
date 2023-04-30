from src import db
from .answer import Answer


class Attempt(db.Model):
    __tablename__ = 'attempts'
    id = db.Column(db.Integer, primary_key=True)
    user_score = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    answers = db.relationship('Answer', backref='attempt')

    def __init__(self, assessment_id: int, user_id: int):
        self.assessment_id = assessment_id
        self.user_id = user_id

    @staticmethod
    def create(assessment_id, user_id):  # create new user
        new_attempt = Attempt(assessment_id=assessment_id,
                              user_id=user_id)
        db.session.add(new_attempt)
        db.session.commit()
        return new_attempt

    def __repr__(self):
        return '<Attempt %r>' % self.id
