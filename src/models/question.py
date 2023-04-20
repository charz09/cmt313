from src import db
# import datetime
# from flask_login import current_user


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    # TODO change to a question type table
    question_type = db.Column(db.String(30), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    choices = db.relationship('Choice', backref='question')
    correct_choice_id = db.Column(db.Integer, db.ForeignKey('choices.id'))
    # created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, content: str, assessment_id: int, question_type: str):
        self.content = content
        self.assessment_id = assessment_id
        self.question_type = question_type

    @staticmethod
    def create(content, assessment_id, question_type):  # create new user
        new_question = Question(
            content=content, assessment_id=assessment_id, question_type=question_type)
        db.session.add(new_question)
        db.session.commit()

    def __repr__(self):
        return '<Question %r>' % self.content
