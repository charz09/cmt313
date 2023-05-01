from src import db


class Module(db.Model):
    __tablename__ = 'modules'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64))
    assessment = db.relationship(
        'Assessment', backref='module', lazy='dynamic')

    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

    @staticmethod
    def create(name, code):  # create new module
        new_module = Module(name=name, code=code)
        db.session.add(new_module)
        db.session.commit()
        return new_module

    def __repr__(self):
        return '<Module %r>' % self.name
