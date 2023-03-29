from flask import Blueprint, render_template
from src import app
from flask_login import login_required

lecturer = Blueprint('lecturer', __name__)

@lecturer.route("/lecturer")
@login_required
def home():
    return render_template('lecturer.html')