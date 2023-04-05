from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from src.models.assessment import Assessment

student = Blueprint('student', __name__)

@student.route("/student")
@login_required
def home():
    return render_template('student/home.html')

@student.route("/take_formative_assessment")
@login_required
def take_formative_assessment():
    assessments = Assessment.query.all()
    return render_template('student/take_formative_assessment.html', assessments=assessments)
    