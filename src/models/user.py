from src import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(
        db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username: str):
        self.username = username

    @staticmethod
    def create(username):  # create new user
        new_user = User(username)
        db.session.add(new_user)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username
