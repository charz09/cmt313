from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '<please generate a new secret key>'

from system import routes
