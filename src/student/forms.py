from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length


class NewAttemptForm(FlaskForm):
    visible = BooleanField('Visible')
    description = TextAreaField('Description')
    module = StringField('Module')
    assessment_type = RadioField('Assessment Type', validators=[DataRequired()], choices=[
        ('Formative', 'Formative'), ('Summative', 'Summative')])
    submit = SubmitField('Create Assessment')


class NewAttemptForm(FlaskForm):
    submit = SubmitField('Submit Attempt')


class FeedbackForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Submit')