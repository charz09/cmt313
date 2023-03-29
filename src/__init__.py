from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('src.config.Config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'entry.login'
login_manager.login_message_category = 'unsuccessful'

# Create tables if they don't exist
with app.app_context():
    from src.models.user import User
    db.create_all()
    
from src.entry.routes import entry
from src.lecturer.routes import lecturer
from src.student.routes import student

app.register_blueprint(entry)
app.register_blueprint(lecturer)
app.register_blueprint(student)