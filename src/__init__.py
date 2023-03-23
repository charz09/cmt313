from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('src.config.Config')
db = SQLAlchemy(app)

# Create tables if they don't exist
with app.app_context():
    from src.models.user import User
    db.create_all()
    
from src import routes