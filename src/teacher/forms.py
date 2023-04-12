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
    content = TextAreaField('Content')
    question_type = RadioField('Question Type', validators=[DataRequired()], choices=[
        ('Multiple Choice', 'Multiple Choice'), ('Single Answer', 'Single Answer')])
    correct_answer = StringField('Correct Answer', validators=[DataRequired()])
    incorrect_answer_1 = StringField(
        'Incorrect Answer', validators=[DataRequired()])
    incorrect_answer_2 = StringField(
        'Incorrect Answer', validators=[DataRequired()])
    incorrect_answer_3 = StringField(
        'Incorrect Answer', validators=[DataRequired()])
    submit = SubmitField('Create Question')


class EditQuestionForm(FlaskForm):
    content = TextAreaField('Content')
    question_type = RadioField('Question Type', validators=[DataRequired()], choices=[
        ('Multiple Choice', 'Multiple Choice'), ('Single Answer', 'Single Answer')])
    correct_answer = StringField('Correct Answer', validators=[DataRequired()])
    incorrect_answer_1 = StringField(
        'Incorrect Answer', validators=[DataRequired()])
    incorrect_answer_2 = StringField(
        'Incorrect Answer', validators=[DataRequired()])
    incorrect_answer_3 = StringField(
        'Incorrect Answer', validators=[DataRequired()])
    submit = SubmitField('Save Changes')
