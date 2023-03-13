from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


from flask import render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = '<please generate a new secret key>'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/")
# @app.route("/home")
def home():
    return render_template('home.html', title='Home')
