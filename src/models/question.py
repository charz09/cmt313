from src import db
import datetime


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, index=True)
    content = db.Column(db.Text)
    number_of_answers = db.Column(db.Integer, default=10)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    # created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

#     # @property
#     # def password(self):
#     #     raise AttributeError('password is not a readable attribute')

#     # @password.setter
#     # def password(self, password):
#     #     self.password_hash = generate_password_hash(password)

#     # def verify_password(self, password):
#     #     return check_password_hash(self.password_hash, password)

    def __init__(self, title: str, content: str, number_of_answers: int):
        self.title = title
        self.content = content
        self.number_of_answers = number_of_answers
        # self.user_id = current_user

#     @staticmethod
#     def create(name):  # create new user
#         new_assessment = Assessment(name)
#         db.session.add(new_assessment)
#         db.session.commit()

#     def __repr__(self):
#         return '<Assessment %r>' % self.name
