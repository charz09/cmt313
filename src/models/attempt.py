from src import db


class Attempt(db.Model):
    __tablename__ = 'attempts'
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, assessment_id: int, created_by: int):
        self.assessment_id = assessment_id
        self.created_by = created_by

    @staticmethod
    def create(assessment_id, created_by):  # create new user
        new_attempt = Attempt(assessment_id=assessment_id,
                              created_by=created_by)
        db.session.add(new_attempt)
        db.session.commit()

    def __repr__(self):
        return '<Attempt %r>' % self.name
