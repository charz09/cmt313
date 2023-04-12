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


class EditAssessmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    visible = BooleanField('Visible')
    description = TextAreaField('Description')
    module = StringField('Module')
    assessment_type = RadioField('Assessment Type', validators=[DataRequired()], choices=[
        ('Formative', 'Formative'), ('Summative', 'Summative')])
    submit = SubmitField('Save Changes')


class NewQuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    number_of_answers = IntegerField('Number of answers')
    submit = SubmitField('Create Question')


class EditQuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    number_of_answers = IntegerField('Number of answers')
    submit = SubmitField('Save Changes')
