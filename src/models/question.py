from src import db
import datetime
from flask_login import current_user


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, index=True)
    content = db.Column(db.Text)
    number_of_answers = db.Column(db.Integer, default=10)
    # created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    # created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

#     # @property
#     # def password(self):
#     #     raise AttributeError('password is not a readable attribute')

#     # @password.setter
#     # def password(self, password):
#     #     self.password_hash = generate_password_hash(password)

#     # def verify_password(self, password):
#     #     return check_password_hash(self.password_hash, password)

    def __init__(self, title: str, content: str, number_of_answers: int, assessment_id: int):
        self.title = title
        self.content = content
        self.number_of_answers = number_of_answers
        self.assessment_id = assessment_id
        # self.created_by = current_user.id

#     @staticmethod
#     def create(name):  # create new user
#         new_assessment = Assessment(name)
#         db.session.add(new_assessment)
#         db.session.commit()

#     def __repr__(self):
#         return '<Assessment %r>' % self.name
