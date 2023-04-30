from src import db


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=False)
    correct_answer = db.Column(db.Text)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content: str, is_correct: bool, correct_answer: str, attempt_id: int, question_id: int, user_id: int):
        self.content = content
        self.question_id = question_id
        self.attempt_id = attempt_id
        self.is_correct = is_correct
        self.correct_answer = correct_answer
        self.user_id = user_id

    @staticmethod
    def create(content, is_correct, correct_answer, attempt_id, question_id, user_id):
        new_answer = Answer(
            content=content, is_correct=is_correct, correct_answer=correct_answer, attempt_id=attempt_id, question_id=question_id, user_id=user_id)
        db.session.add(new_answer)
        db.session.commit()
        return new_answer

    def __repr__(self):
        return '<Answer %r>' % self.content
