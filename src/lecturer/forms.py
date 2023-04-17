from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length
from src.models.assessment import Assessment

class CreateAssessmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    assessment_type = RadioField('Assessment Type', choices=[('formative', 'Formative Assessment'), ('summative', 'Summative Assessment')], default='')
    submit = SubmitField('Create Assessment')

class EditAssessmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    assessment_type = RadioField('Assessment Type', choices=[('formative', 'Formative Assessment'), ('summative', 'Summative Assessment')], default='')
    submit = SubmitField('Update Assessment')

class CreateQuestionForm(FlaskForm):
    question = StringField('Question Text', validators=[DataRequired(), Length(min=5, max=100)])
    question_type = SelectField('Question Type', choices=[('', 'Select Question Type'), ('multiple_choice', 'Multiple Choice'), ('fill_in_the_blank', 'Fill-in the Blank')], default='')
    answer = StringField('Answer', validators=[DataRequired()])
    choice_1 = StringField('Choice 1', validators=[Length(max=100)])
    choice_2 = StringField('Choice 2', validators=[Length(max=100)])
    choice_3 = StringField('Choice 3', validators=[Length(max=100)])
    submit = SubmitField('Create Question')