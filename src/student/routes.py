from flask import Blueprint, render_template
from flask import current_app
from flask_login import login_required

student = Blueprint('student', __name__)

@student.route("/student")
@login_required
def home():
    return render_template('student/home.html')