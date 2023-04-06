from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from src.models.assessment import Assessment
from src.models.question import Question, Choice


student = Blueprint('student', __name__)

@student.route("/student")
@login_required
def home():
    return render_template('student/home.html')

@student.route("/view_assessments")
@login_required
def view_assessments():
    assessments = Assessment.query.all()
    return render_template('student/view_assessments.html', assessments=assessments)

@student.route("/view_formative_assessments")
@login_required
def view_formative_assessments():
    assessments = Assessment.query.filter_by(assessment_type='formative').all()
    return render_template('student/view_formative_assessments.html', assessments=assessments)


@student.route("/submit_summative_assessment")
@login_required
def submit_summative_assessment():
    assessments = Assessment.query.filter_by(assessment_type='summative').all()
    return render_template('student/submit_summative_assessment.html', assessments=assessments)


@student.route('/attempt_assessment/<int:assessment_id>')
def attempt_assessment(assessment_id):
    # Retrieve the assessment object from the database
    assessment = Assessment.query.get(assessment_id)

    # If assessment does not exist, redirect to home page
    if assessment is None:
        return redirect(url_for('student.home'))

    # Get all questions for the assessment
    questions = Question.query.filter_by(assessment_id=assessment.id).all()

    return render_template('student/assessment.html', assessment=assessment, questions=questions)

