from src import db


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, content: str, question_id: int, answer_type: str):
        self.content = content
        self.question_id = question_id

    @staticmethod
    def create(content, question_id):
        new_answer = Answer(
            content=content, question_id=question_id)
        db.session.add(new_answer)
        db.session.commit()

    def __repr__(self):
        return '<Answer %r>' % self.name
