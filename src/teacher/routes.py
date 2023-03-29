from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import login_required
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from src import db
from ..models.assessment import Assessment
from ..models.question import Question
from . import teacher


class NewAssessmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    visible = BooleanField('Visible')
    description = TextAreaField('Description')
    module = StringField('Module')
    number_of_questions = IntegerField('Number of questions')
    submit = SubmitField('Create Assessment')


class EditAssessmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    visible = BooleanField('Visible')
    description = TextAreaField('Description')
    module = StringField('Module')
    number_of_questions = IntegerField('Number of questions')
    submit = SubmitField('Save Changes')


# VIEW ASSESSMENTS
@teacher.route('/', methods=['GET'])
@teacher.route('/assessments', methods=['GET'])
@login_required
def assessments_index():
    assessments = Assessment.query.all()
    return render_template('teacher/assessments/index.html', assessments=assessments)

# SHOW + DELETE


@teacher.route('/assessments/<int:id>', methods=['GET', 'POST'])
@login_required
def show_assessment(id):
    print("method", request.method)
    if request.method == 'POST':
        assessment = Assessment.query.filter_by(id=id).first()
        db.session.delete(assessment)
        db.session.commit()
        return redirect(url_for('teachers.assessments_index'))

    assessment = Assessment.query.filter_by(id=id).first()
    return render_template('teacher/assessments/show.html', assessment=assessment)


# NEW ASSESSMENT
@teacher.route('/assessments/new', methods=['GET', 'POST'])
@login_required
def new_assessment():
    form = NewAssessmentForm()
    form.number_of_questions.data = 10
    if request.method == 'POST':
        if form.validate_on_submit():
            assessment = Assessment(name=form.name.data,
                                    visible=form.visible.data,
                                    description=form.description.data,
                                    module=form.module.data,
                                    number_of_questions=form.number_of_questions.data)
            db.session.add(assessment)
            db.session.commit()
            return redirect(url_for('teachers.assessments_index'))
    return render_template('teacher/assessments/new.html', form=form)


# EDIT ASSESSMENT
@teacher.route('/assessments/<int:id>/edit', methods=['GET', 'POST'])
def edit_assessment(id):
    form = EditAssessmentForm()
    assessment = Assessment.query.filter_by(id=id).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            assessment.name = form.name.data
            assessment.visible = form.visible.data
            assessment.description = form.description.data
            assessment.module = form.module.data
            assessment.number_of_questions = form.number_of_questions.data
            db.session.add(assessment)
            db.session.commit()
            return redirect(url_for('teachers.assessments_index'))
    print(assessment.name)
    form.name.data = assessment.name
    form.visible.data = assessment.visible
    form.description.data = assessment.description
    form.module.data = assessment.module
    form.number_of_questions.data = assessment.number_of_questions

    return render_template('teacher/assessments/edit.html', form=form)


# VIEW QUESTIONS
@teacher.route('/questions', methods=['GET'])
@login_required
def questions_index():
    questions = Question.query.all()
    return render_template('teacher/questions/index.html', questions=questions)


# SHOW + DELETE QUESTION
@teacher.route('/questions/<int:id>', methods=['GET', 'POST'])
@login_required
def show_question(id):
    if request.method == 'POST':
        question = Question.query.filter_by(id=id).first()
        db.session.delete(question)
        db.session.commit()
        return redirect(url_for('teachers.questions_index'))

    question = question.query.filter_by(id=id).first()
    return render_template('teacher/questions/show.html', question=question)


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

# NEW QUESTION
@teacher.route('/questions/new', methods=['GET', 'POST'])
@login_required
def new_question():
    form = NewQuestionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            question = Question(title=form.title.data,
                                content=form.content.data,
                                number_of_answers=form.number_of_answers.data)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('teachers.questions_index'))
    return render_template('teacher/questions/new.html', form=form)

# EDIT ASSESSMENT


@teacher.route('/questions/<int:id>/edit', methods=['GET', 'POST'])
def edit_question(id):
    form = EditQuestionForm()
    question = Question.query.filter_by(id=id).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            question.title = form.title.data
            question.content = form.content.data
            question.number_of_answers = form.number_of_answers.data
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('teachers.questions_index'))

    form.title.data = question.title
    form.content.data = question.content
    form.number_of_answers.data = question.number_of_answers

    return render_template('teacher/questions/edit.html', form=form)
