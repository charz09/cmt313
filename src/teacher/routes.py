from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from src import db
from ..models.assessment import Assessment
from ..models.question import Question
from .forms import NewAssessmentForm, NewQuestionForm, EditAssessmentForm, EditQuestionForm
from . import teacher


# VIEW ASSESSMENTS
@teacher.route('/', methods=['GET'])
@teacher.route('/assessments', methods=['GET'])
@login_required
def assessments_index():
    assessments = Assessment.query.all()
    return render_template('teacher/assessments/index.html', assessments=assessments)


# NEW ASSESSMENT
@teacher.route('/assessments/new', methods=['GET', 'POST'])
@login_required
def new_assessment():
    form = NewAssessmentForm()
    if form.validate_on_submit():
        assessment = Assessment(name=form.name.data,
                                visible=form.visible.data,
                                description=form.description.data,
                                module=form.module.data,
                                assessment_type=form.assessment_type.data)
        db.session.add(assessment)
        db.session.commit()
        flash('Assessment created successfully!')
        return redirect(url_for('teachers.assessments_index'))
    return render_template('teacher/assessments/new.html', form=form)

# SHOW + DELETE


@teacher.route('/assessments/<int:id>', methods=['GET', 'POST'])
@login_required
def show_assessment(id):
    if request.method == 'POST':
        assessment = Assessment.query.filter_by(id=id).first()
        db.session.delete(assessment)
        db.session.commit()
        flash('Assessment deleted successfully!')
        return redirect(url_for('teachers.assessments_index'))

    assessment = Assessment.query.filter_by(id=id).first()
    return render_template('teacher/assessments/show.html', assessment=assessment)


# EDIT ASSESSMENT
@teacher.route('/assessments/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_assessment(id):
    form = EditAssessmentForm()
    assessment = Assessment.query.first_or_404(id)
    if form.validate_on_submit():
        assessment.name = form.name.data
        assessment.visible = form.visible.data
        assessment.description = form.description.data
        assessment.module = form.module.data
        assessment.assessment_type = form.assessment_type.data
        db.session.add(assessment)
        db.session.commit()
        return redirect(url_for('teachers.assessments_index'))

    form.name.data = assessment.name
    form.visible.data = assessment.visible
    form.description.data = assessment.description
    form.module.data = assessment.module
    form.assessment_type.data = assessment.assessment_type

    return render_template('teacher/assessments/edit.html', form=form)


# # NEW QUESTION
# @teacher.route('/assessments/<int:id>/new_question', methods=['GET', 'POST'])
# @login_required
# def new_question(id):
#     form = NewQuestionForm()
#     if form.validate_on_submit():
#         question = Question(title=form.title.data,
#                             content=form.content.data,
#                             number_of_answers=form.number_of_answers.data,
#                             assessment_id=id)
#         db.session.add(question)
#         db.session.commit()
#         flash('Question created successfully!')
#         return redirect(url_for('teachers.show_assessment', id=id))
#     return render_template('teacher/questions/new.html', form=form)

# # EDIT QUESTION
# @teacher.route('/questions/<int:id>/edit', methods=['GET', 'POST'])
# def edit_question(id):
#     form = EditQuestionForm()
#     question = Question.query.filter_by(id=id).first()
#     if form.validate_on_submit():
#         question.title = form.title.data
#         question.content = form.content.data
#         question.number_of_answers = form.number_of_answers.data
#         db.session.add(question)
#         db.session.commit()
#         return redirect(url_for('teachers.questions_index'))

#     form.title.data = question.title
#     form.content.data = question.content
#     form.number_of_answers.data = question.number_of_answers

#     return render_template('teacher/questions/edit.html', form=form)
