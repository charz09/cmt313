from flask_wtf import FlaskForm
from wtforms import SubmitField


class NewAttemptForm(FlaskForm):
    submit = SubmitField('Submit Attempt')
