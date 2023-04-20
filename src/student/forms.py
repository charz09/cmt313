from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, IntegerField, RadioField
from wtforms.validators import DataRequired


class NewAssessmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    visible = BooleanField('Visible')
    description = TextAreaField('Description')
    module = StringField('Module')
    assessment_type = RadioField('Assessment Type', validators=[DataRequired()], choices=[
        ('Formative', 'Formative'), ('Summative', 'Summative')])
    submit = SubmitField('Create Assessment')
