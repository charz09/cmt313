from flask import render_template
from . import student
from ..models.assessment import Assessment
from flask_login import login_required, current_user

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


@student.route('/attempts/<int:id>/new')
@login_required
def new_attempt(id):
    assessment = Assessment.query.get(id)
    questions = assessment.questions

    class NewAttemptForm(FlaskForm):
        submit = SubmitField('Submit Attempt')
    i = 0
    for question in questions:
        setattr(NewAttemptForm, f"question_{i}", StringField(question.content))
        i += 1

    form = NewAttemptForm()

    return render_template('student/attempts/new.html', assessment=assessment, form=form)


# View assessment attempt

# Edit assessment attempt

# Delete assessment attempt


# View question attempt

# Edit question attempt

# Delete question attempt
