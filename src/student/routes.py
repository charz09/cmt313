from flask import render_template, redirect, url_for, request
from . import student
from ..models.assessment import Assessment
from ..models.attempt import Attempt
from ..models.answer import Answer
from flask_login import login_required, current_user
from .forms import NewAttemptForm
from wtforms import StringField, RadioField

@student.route('/')
@login_required
def index():
    return render_template('student/attempts/index.html')


# View formative assessment
@student.route('/formative')
@login_required
def view_formative():
    assessments = Assessment.query.filter_by(assessment_type='Formative', visible=True).all()
    return render_template('student/attempts/view_formative.html', assessments=assessments)


# View instructions for an assessment
@student.route('/assessment_instructions/<int:assessment_id>')
@login_required
def view_instructions(assessment_id):
    # Retrieve the assessment object from the database
    assessment = Assessment.query.get(assessment_id)

    return render_template('student/attempts/instruction.html', assessment=assessment)




@student.route('/attempt_assessment/<int:assessment_id>', methods=['GET', 'POST'])
@login_required
def attempt_assessment(assessment_id):
    assessment = Assessment.query.get(assessment_id)

    attempt = None
    num_attempts = request.args.get('num_attempts')
    if request.method == 'POST':
        attempt = int(request.form.get('attempts'))

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

    if num_attempts and int(num_attempts) > 1:
        return render_template('student/attempts/score.html', assessment=assessment, num_attempts=num_attempts)
    else:
        return render_template('student/attempts/new2.html', assessment=assessment, form=form, num_attempts=attempt)


@student.route('/mark_assessment/<int:assessment_id>/<int:num_attempts>', methods=['POST'])
@login_required
def mark_assessment(assessment_id, num_attempts):

    form = NewAttemptForm()
    assessment = Assessment.query.get(assessment_id)
    attempt = Attempt.create(assessment.id, current_user.id)

    for i, question in enumerate(assessment.questions):
        correct_choice = [
            choice for choice in question.choices if choice.is_correct == True][0].content
        user_choice = getattr(form, f"question_{i}").data

        if user_choice == correct_choice:
            Answer.create(
                user_choice, True, correct_choice, attempt.id, question.id)
        else:
            Answer.create(
                user_choice, False, correct_choice, attempt.id, question.id)

    attempt_answers = Answer.query.filter_by(attempt_id=attempt.id).all()
    user_score = sum([answer.is_correct for answer in attempt_answers])
    total_score = len(attempt_answers)
    percentage_score = '{:.0%}'.format(user_score / total_score)

    if num_attempts > 1:
        return render_template('student/attempts/score.html', attempt=attempt, user_score=user_score, total_score=total_score, percentage_score=percentage_score)
    else:
        return render_template('student/attempts/formative_result.html', attempt=attempt, user_score=user_score, total_score=total_score, percentage_score=percentage_score)





# ############################################








# View summative assessment
@student.route('/summative')
@login_required
def view_summative():
    assessments = Assessment.query.filter_by(assessment_type='Summative', visible=True).all()
    return render_template('student/attempts/view_summative.html', assessments=assessments)


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



