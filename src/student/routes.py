from flask import render_template, redirect, url_for
from . import student
from ..models.assessment import Assessment
from ..models.attempt import Attempt
from flask_login import login_required, current_user
from .forms import NewAttemptForm
from src import db

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, IntegerField, RadioField
from wtforms.validators import DataRequired


# View all assessment attempts
@student.route('/')
@login_required
def index():
    assessments = Assessment.query.all()
    return render_template('student/attempts/index.html', assessments=assessments)

# Create new Assessment attempt


@student.route('/attempts/<int:id>/new', methods=['GET', 'POST'])
@login_required
def new_attempt(id):
    assessment = Assessment.query.get(id)
    questions = assessment.questions

    for i, question in enumerate(questions):
        if question.question_type == "Multiple Choice":
            choices = []
            for choice in question.choices:
                choices.append((choice.content, choice.content))
                setattr(NewAttemptForm, f"question_{i}",
                        RadioField(question.content,  choices=choices, render_kw={"data-question-id": f"{question.id}"}))
        else:
            setattr(NewAttemptForm, f"question_{i}", StringField(
                question.content, render_kw={"data-question-id": f"{question.id}"}))

    form = NewAttemptForm()

    if form.validate_on_submit():
        attempt = Attempt(assessment_id=assessment.id,
                          created_by=current_user.id)
        db.session.add(attempt)
        db.session.commit()

        return redirect(url_for('students.index'))

    return render_template('student/attempts/new.html', assessment=assessment, form=form)


# View assessment attempt
# show view that will show the marked assessment . . .
