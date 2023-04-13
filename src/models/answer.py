from src import db


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, content: str, is_correct: bool, question_id: int):
        self.content = content
        self.question_id = question_id
        self.is_correct = is_correct

    @staticmethod
    def create(content, is_correct, question_id):
        new_answer = Answer(
            content=content, is_correct=is_correct, question_id=question_id)
        db.session.add(new_answer)
        db.session.commit()

    def __repr__(self):
        return '<Answer %r>' % self.name
