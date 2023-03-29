from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from src.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'entry.login'
login_manager.login_message_category = 'unsuccessful'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from src.entry.routes import entry
    from src.lecturer.routes import lecturer
    from src.student.routes import student
    app.register_blueprint(entry)
    app.register_blueprint(lecturer)
    app.register_blueprint(student)

    # Create tables if they don't exist
    with app.app_context():
        from src.models.user import User
        db.create_all()

    return app
