from flask import render_template, redirect, url_for, request
from . import student
from ..models.assessment import Assessment
from ..models.attempt import Attempt
from ..models.answer import Answer
from flask_login import login_required, current_user
from .forms import NewAttemptForm
from wtforms import StringField, RadioField
# from src import db
# from wtforms.validators import DataRequired


# View all assessment attempts
@student.route('/')
@login_required
def index():
    assessments = Assessment.query.all()
    return render_template('student/attempts/index.html', assessments=assessments)


# Create new Assessment attempt
@student.route('/assessments/<int:id>/attempt/new', methods=['GET', 'POST'])
@login_required
def new_attempt(id):
    assessment = Assessment.query.get(id)

    # Build a form dynamically, for whatever questions are in the assessment.
    for i, question in enumerate(assessment.questions):
        if question.question_type == "Multiple Choice":
            # Build a tuple of choices for the radio button.
            choices = []
            for choice in question.choices:
                choices.append((choice.content, choice.content))
                # set the attribute on the form under the value "question_?"
                setattr(NewAttemptForm, f"question_{i}", RadioField(
                    question.content,  choices=choices))
        else:
            # set the attribute on the form under the value "question_?"
            setattr(NewAttemptForm, f"question_{i}", StringField(
                question.content, render_kw={"data-question-id": f"{question.id}"}))

    form = NewAttemptForm()

    # on_validate was not working, so switeched to:
    if request.method == "POST":
        attempt = Attempt.create(assessment.id,
                                 current_user.id)

        # Creates the Answer objects and stores the users answer, the correct answer etc..
        for i, question in enumerate(assessment.questions):
            # Search the questions choices for the correct choice
            correct_choice = [
                choice for choice in question.choices if choice.is_correct == True][0].content

            # get the users answer dynamically from the form object
            user_choice = getattr(form, f"question_{i}").data

            if user_choice == correct_choice:
                Answer.create(
                    user_choice, True, correct_choice, attempt.id, question.id)
            else:
                Answer.create(
                    user_choice, False, correct_choice, attempt.id, question.id)

        return redirect(url_for('students.results', id=attempt.id))

    return render_template('student/attempts/new.html', form=form)


# See the results of an attempt
@student.route('/attempts/<int:id>/results', methods=['GET'])
@login_required
def results(id):
    attempt = Attempt.query.get(id)
    return render_template('student/attempts/results.html', attempt=attempt)
