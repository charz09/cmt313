from src import db
from .attempt import Attempt
from datetime import datetime


class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    assessment_type = db.Column(db.String(50), nullable=False)
    visible = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
    module = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    questions = db.relationship('Question', backref='assessment')
    attempts = db.relationship('Attempt', backref='assessment')

    # time related insance varaiables
    created_at = db.Column(db.DateTime, default=datetime.now())
    available_from = db.Column(db.DateTime, default=datetime.now())
    feedback_from = db.Column(db.DateTime, default=datetime.now())
    availiable_to = db.Column(db.DateTime)

    def __init__(self, name: str, visible: bool, description: str, module: str, assessment_type: str, user_id: int):
        self.name = name
        self.assessment_type = assessment_type
        self.visible = visible
        self.description = description
        self.module = module
        self.user_id = user_id

    @staticmethod
    def create(name, visible, description, module, assessment_type, user_id):  # create new Assessment
        new_assessment = Assessment(name=name,
                                    visible=visible,
                                    description=description,
                                    module=module,
                                    assessment_type=assessment_type,
                                    user_id=user_id)
        db.session.add(new_assessment)
        db.session.commit()
        return new_assessment

    def __repr__(self):
        return '<Assessment %r>' % self.name
