from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '<please generate a new secret key>'

from system.data import database
from system import routes
from system.models.user import User
from system.models.role import Role