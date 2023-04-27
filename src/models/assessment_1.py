from src import db
from .attempt import Attempt


class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    # TODO change to be a table
    assessment_type = db.Column(db.String(50), nullable=False)
    visible = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
    module = db.Column(db.String(64), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    questions = db.relationship(
        'Question', backref='assessment')
    attempts = db.relationship(
        'Attempt', backref='assessment')
    
    # add feedback to the assessment module:
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'))
    feedback = db.relationship('Feedback', backref='assessment')


    # created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, name: str, visible: bool, description: str, module: str, assessment_type: str):
        self.name = name
        self.assessment_type = assessment_type
        self.visible = visible
        self.description = description
        self.module = module

    @staticmethod
    def create(name, visible, description, module, assessment_type):  # create new user
        new_assessment = Assessment(
            name=name, visible=visible, description=description, module=module, assessment_type=assessment_type)
        db.session.add(new_assessment)
        db.session.commit()

    def __repr__(self):
        return '<Assessment %r>' % self.name
