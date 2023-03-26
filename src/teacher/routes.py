from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from . import teacher
from ..models.assessment import Assessment
from src import db


class NewAssessmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    visible = BooleanField('Visible')
    description = TextAreaField('Description')
    module = StringField('Module')
    number_of_questions = IntegerField('Number of questions')
    submit = SubmitField('Log In')


# View All Assessments
@teacher.route('/', methods=['GET', 'POST'])
@teacher.route('/assessments', methods=['GET', 'POST'])
def index():
    form = NewAssessmentForm()
    assessments = Assessment.query.all()

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

    return render_template('teacher/assessments/index.html', form=form, assessments=assessments)

# # Show Assessment
# @teacher.route('/assessments/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# def show(id):
#     return render_template('teacher/assessments/show.html')

# # New Assessment
# @teacher.route('/assessments/new', methods=['GET'])
# def new():
#     form = NewAssessmentForm()
#     form.number_of_questions.data = 10
#     return render_template('teacher/assessments/new.html', form=form)

# # Create Assessment
# @teacher.route('/assessments', methods=['POST'])
# def create():
#     if form.validate_on_submit():
#         assessment = Assessment(name=form.name.data, visible=form.visible.data, description=form.description.data)
#     return render_template('teacher/assessments/index.html')

# # Edit Assessment
# @teacher.route('/assessments/<int:id>/edit', methods=['GET'])
# def edit(id):
#     return render_template('teacher/assessments/edit.html')

# # Update assessment
# @teacher.route('/assessments/<int:id>/', methods=['PATCH'])
# def update(id):
#     # Update the assessment with id=id
#     return render_template('teacher/assessments/index.html')

# # Delete Assessment
# @teacher.route('/assessments/<int:id>/', methods=['DELETE'])
# def destroy(id):
#     # Delete post with id=id
#     return render_template('teacher/assessments/index.html')
