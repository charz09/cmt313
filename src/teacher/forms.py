from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, IntegerField, RadioField, DateTimeLocalField, SelectField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired
from src.models.module import Module


class NewAssessmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    visible = BooleanField('Visible')
    description = TextAreaField('Description')
    module_id = SelectField('Module', choices=[])
    assessment_type = RadioField('Assessment Type', validators=[DataRequired()], choices=[
        ('Formative', 'Formative'), ('Summative', 'Summative')], default='Summative')

    available_from = DateTimeLocalField(
        'Available From', format='%Y-%m-%d %H:%M')
    available_to = DateTimeLocalField(
        'Assessment Deadline', format='%Y-%m-%d %H:%M')
    feedback_from = DateTimeLocalField(
        'Feedback return from', format='%Y-%m-%d %H:%M')

    submit = SubmitField('Create Assessment')


class EditAssessmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    visible = BooleanField('Visible')
    description = TextAreaField('Description')
    module_id = StringField('Module')
    assessment_type = RadioField('Assessment Type', validators=[DataRequired()], choices=[
        ('Formative', 'Formative'), ('Summative', 'Summative')])

    available_from = DateTimeLocalField(
        'Available From', format='%Y-%m-%d %H:%M')
    available_to = DateTimeLocalField(
        'Assessment Deadline', format='%Y-%m-%d %H:%M')
    feedback_from = DateTimeLocalField(
        'Feedback return from', format='%Y-%m-%d %H:%M')

    submit = SubmitField('Save Changes')


class NewQuestionForm(FlaskForm):
    content = TextAreaField('Content')
    question_type = RadioField('Question Type', validators=[DataRequired()], choices=[
        ('Multiple Choice', 'Multiple Choice'), ('Single Answer', 'Single Answer')])
    correct_choice = StringField('Correct choice', validators=[DataRequired()])
    incorrect_choice_1 = StringField(
        'Incorrect Answer')
    incorrect_choice_2 = StringField(
        'Incorrect Answer')
    incorrect_choice_3 = StringField(
        'Incorrect Answer')
    submit = SubmitField('Create Question')


class EditQuestionForm(FlaskForm):
    content = TextAreaField('Content')
    question_type = RadioField('Question Type', validators=[DataRequired()], choices=[
        ('Multiple Choice', 'Multiple Choice'), ('Single Answer', 'Single Answer')])
    correct_choice = StringField('Correct Answer', validators=[DataRequired()])
    incorrect_choice_1 = StringField(
        'Incorrect Answer')
    incorrect_choice_2 = StringField(
        'Incorrect Answer')
    incorrect_choice_3 = StringField(
        'Incorrect Answer')
    submit = SubmitField('Save Changes')
