from flask import render_template, redirect, url_for, request
from . import student
from ..models.assessment import Assessment
from ..models.attempt import Attempt
from ..models.answer import Answer
from flask_login import login_required, current_user
from .forms import NewAttemptForm
from wtforms import StringField, RadioField
from datetime import datetime
from src import db
# from wtforms.validators import DataRequired


@student.before_request  # protects the route against student access
def check_user_is_teacher():
    if current_user.role.name == "Teacher":
        return redirect(url_for('teachers.index'))


@student.route('/')  # View all assessment attempts
@login_required
def index():
    assessments = Assessment.query.all()
    return render_template('student/index.html', assessments=assessments)


@student.route('/assessments/formative')  # View all assessment attempts
@login_required
def formative_index():
    assessments = Assessment.query.filter_by(assessment_type='Formative')
    return render_template('student/attempts/summative/index.html', assessments=assessments)


@student.route('/assessments/summative')  # View all assessment attempts
@login_required
def summative_index():
    assessments = Assessment.query.filter_by(assessment_type='Summative')
    attempts = Attempt.query.filter_by(user_id=current_user.id).all()
    return render_template('student/attempts/summative/index.html', assessments=assessments, attempts=attempts, datetime=datetime)


# Create new Assessment attempt
@student.route('/assessments/<int:id>/attempt/new', methods=['GET', 'POST'])
@login_required
def new_attempt(id):
    assessment = Assessment.query.get(id)

    # protect the route from access before the assessment is available
    if datetime.utcnow() < assessment.available_from:
        return redirect(url_for('students.summative_index'))

    # protect the route from access after the deadline
    if datetime.utcnow() < assessment.available_from:
        return redirect(url_for('students.summative_index'))

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

    # check to see if the student has attempted the question before
    attempt = Attempt.query.filter_by(
        assessment_id=assessment.id, user_id=current_user.id).first()

    # if so redirect them to edit their attempt
    if attempt:
        return redirect(url_for('students.edit_attempt', id=attempt.id))

    # on_validate was not working, so switeched to:
    if request.method == "POST":

        # if the deadline has passed redirect them to the home screen.
        if datetime.utcnow() > assessment.available_to:
            return redirect(url_for('students.summative_index'))

        attempt = Attempt.create(assessment.id,
                                 current_user.id)

        # Creates the Answer objects and stores the users answer, the correct answer etc..
        for i, question in enumerate(assessment.questions):
            # Search the questions choices for the correct choice
            correct_choice = [
                choice for choice in question.choices if choice.is_correct == True][0].content

            # get the users answer dynamically from the form object
            user_choice = getattr(form, f"question_{i}").data

            # create Answer and assigns if it was correct or not.
            if user_choice == correct_choice:
                Answer.create(
                    user_choice, True, correct_choice, attempt.id, question.id, current_user.id)
            else:
                Answer.create(
                    user_choice, False, correct_choice, attempt.id, question.id, current_user.id)

        return redirect(url_for('students.results', id=attempt.id))

    # render the template with the dynamically created form
    return render_template('student/attempts/summative/new.html', form=form, assessment=assessment)


# EDIT ASSESSMENT ATTEMPT
@student.route('/attempt/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_attempt(id):
    attempt = Attempt.query.get(id)
    assessment = attempt.assessment

    # protect the route from access before the assessment is available
    if datetime.utcnow() < assessment.available_from:
        return redirect(url_for('students.summative_index'))

    # protect the route from access after the deadline
    if datetime.utcnow() < assessment.available_from:
        return redirect(url_for('students.summative_index'))

    answers = attempt.answers

    # Build a form dynamically, for whatever questions are in the assessment.
    for i, question in enumerate(assessment.questions):
        if question.question_type == "Multiple Choice":
            # Build a tuple of choices for the radio button.
            choices = []
            for choice in question.choices:
                choices.append((choice.content, choice.content))
                # set the attribute on the form under the value "question_?"
                setattr(NewAttemptForm, f"question_{i}", RadioField(
                    question.content,  choices=choices, default=answers[i].content))
        else:
            # set the attribute on the form under the value "question_?"
            setattr(NewAttemptForm, f"question_{i}", StringField(
                question.content))

    form = NewAttemptForm()

    # on_validate was not working, so switeched to:
    if request.method == "POST":

        # if the deadline has passed redirect them to the home screen.
        if datetime.utcnow() > assessment.available_to:
            return redirect(url_for('students.summative_index'))

        # Creates the Answer objects and stores the users answer, the correct answer etc..
        for i, question in enumerate(assessment.questions):

            answer = Answer.query.filter_by(
                question_id=question.id, user_id=current_user.id).first()

            # Search the questions choices for the correct choice
            correct_choice = [
                choice for choice in question.choices if choice.is_correct == True][0].content

            # get the users answer dynamically from the form object
            user_choice = getattr(form, f"question_{i}").data

            # update answer with if it was correct or not.
            if user_choice == correct_choice:
                answer.is_correct = True
            else:
                answer.is_correct = False

            db.session.commit()

        return redirect(url_for('students.results', id=attempt.id))

    # # render the template with the dynamically created form
    return render_template('student/attempts/summative/edit.html', form=form, assessment=assessment)


# See the results of an attempt
@student.route('/assessments/<int:id>/results', methods=['GET'])
@login_required
def results(id):
    assessment = Assessment.query.get(id)
    attempt = Attempt.query.filter_by(
        assessment_id=id, user_id=current_user.id).first()

    print(datetime.utcnow(), assessment.feedback_from)

    # protect the route from access before the assessment is available
    if datetime.utcnow() < assessment.available_from:
        return redirect(url_for('students.summative_index'))

    # # if the feedback deadline has not passed, only confrim their answers.
    if datetime.utcnow() > assessment.feedback_from:
        return render_template('student/attempts/summative/results.html', attempt=attempt, feedback=True, datetime=datetime)

    # if the feedback deadline has passed, show the feedback as well as their naswers.
    return render_template('student/attempts/summative/results.html', attempt=attempt, feedback=False, datetime=datetime)
