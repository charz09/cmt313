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
    number_of_questions = db.Column(db.Integer, default=0)
    pass_mark = db.Column(db.Integer, default=0)

    # automaticall assigned variables
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    questions = db.relationship('Question', backref='assessment')
    attempts = db.relationship('Attempt', backref='assessment')

    # time related insance varaiables
    available_from = db.Column(db.DateTime, default=datetime.now())
    feedback_from = db.Column(db.DateTime, default=datetime.now())
    available_to = db.Column(db.DateTime)

    def __init__(self,
                 name: str,
                 visible: bool,
                 description: str,
                 module: str,
                 assessment_type: str,
                 user_id: int,
                 available_from: datetime,
                 available_to: datetime,
                 feedback_from: datetime):
        self.name = name
        self.assessment_type = assessment_type
        self.visible = visible
        self.description = description
        self.module = module
        self.user_id = user_id
        self.available_from = available_from
        self.available_to = available_to
        self.feedback_from = feedback_from

    @staticmethod
    def create(name,
               visible,
               description,
               module,
               assessment_type,
               user_id,
               available_from,
               available_to,
               feedback_from):  # create new Assessment
        new_assessment = Assessment(name=name,
                                    visible=visible,
                                    description=description,
                                    module=module,
                                    assessment_type=assessment_type,
                                    user_id=user_id,
                                    available_from=available_from,
                                    available_to=available_to,
                                    feedback_from=feedback_from)
        db.session.add(new_assessment)
        db.session.commit()
        return new_assessment

    def __repr__(self):
        return '<Assessment %r>' % self.name
