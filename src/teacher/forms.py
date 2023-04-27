from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length


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

class NewCommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Submit')

class FeedbackForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=2, max=500)])
    student_id = IntegerField('Student ID', validators=[DataRequired()])
    teacher_seen = BooleanField('Teacher Seen')
    submit = SubmitField('Submit')
