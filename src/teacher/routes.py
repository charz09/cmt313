from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import login_required
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from src import db
from ..models.assessment import Assessment
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
def index():
    assessments = Assessment.query.all()
    return render_template('teacher/assessments/index.html', assessments=assessments)

# SHOW + DELETE
@teacher.route('/assessments/<int:id>', methods=['GET', 'POST'])
@login_required
def show(id):
    print("method", request.method)
    if request.method == 'POST':
        assessment = Assessment.query.filter_by(id=id).first()
        db.session.delete(assessment)
        db.session.commit()
        return redirect(url_for('teachers.index'))

    assessment = Assessment.query.filter_by(id=id).first()
    return render_template('teacher/assessments/show.html', assessment=assessment)


# NEW ASSESSMENT
@teacher.route('/assessments/new', methods=['GET', 'POST'])
@login_required
def new():
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
            return redirect(url_for('teachers.index'))
    return render_template('teacher/assessments/new.html', form=form)


# EDIT ASSESSMENT
@teacher.route('/assessments/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    form = EditAssessmentForm()
    assessment = Assessment.query.filter_by(id=id).first()
    if request.method == 'POST':
        print("route is a patch")
        if form.validate_on_submit():
            print("route is valid")
            assessment.name = form.name.data
            assessment.visible = form.visible.data
            print("a:", assessment.description)
            print("f:", form.description.data)
            assessment.description = form.description.data
            assessment.module = form.module.data
            assessment.number_of_questions = form.number_of_questions.data
            db.session.add(assessment)
            db.session.commit()
            return redirect(url_for('teachers.index'))
    print(assessment.name)
    form.name.data = assessment.name
    form.visible.data = assessment.visible
    form.description.data = assessment.description
    form.module.data = assessment.module
    form.number_of_questions.data = assessment.number_of_questions

    return render_template('teacher/assessments/edit.html', form=form)
