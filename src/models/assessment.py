from src import db
import datetime


class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    visible = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
    module = db.Column(db.String(64), index=True)
    number_of_questions = db.Column(db.Integer, default=10)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

#     # @property
#     # def password(self):
#     #     raise AttributeError('password is not a readable attribute')

#     # @password.setter
#     # def password(self, password):
#     #     self.password_hash = generate_password_hash(password)

#     # def verify_password(self, password):
#     #     return check_password_hash(self.password_hash, password)

    def __init__(self, name: str, visible: bool, description: str, module: str, number_of_questions: int):
        self.name = name
        self.visible = visible
        self.description = description
        self.module = module
        self.number_of_questions = number_of_questions
        # self.user_id = current_user

#     @staticmethod
#     def create(name):  # create new user
#         new_assessment = Assessment(name)
#         db.session.add(new_assessment)
#         db.session.commit()

#     def __repr__(self):
#         return '<Assessment %r>' % self.name
