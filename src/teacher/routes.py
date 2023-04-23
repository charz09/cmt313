from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from src import db
from ..models.user import User
from ..models.assessment import Assessment
from ..models.attempt import Attempt
from ..models.question import Question
from ..models.choice import Choice
from ..models.answer import Answer
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


# NEW QUESTION
@teacher.route('/assessments/<int:id>/new_question', methods=['GET', 'POST'])
@login_required
def new_question(id):
    form = NewQuestionForm()
    if form.validate_on_submit():
        question = Question(
            content=form.content.data,
            question_type=form.question_type.data,
            assessment_id=id)
        db.session.add(question)
        db.session.commit()
        Choice.create(form.correct_choice.data, True, question.id)
        if question.question_type == 'Multiple Choice':
            Choice.create(form.incorrect_choice_1.data, False, question.id)
            Choice.create(form.incorrect_choice_2.data, False, question.id)
            Choice.create(form.incorrect_choice_3.data, False, question.id)

        flash('Question created successfully!')
        return redirect(url_for('teachers.show_assessment', id=id))
    return render_template('teacher/questions/new.html', form=form)


# EDIT QUESTION
@teacher.route('/questions/<int:id>/edit', methods=['GET', 'POST'])
def edit_question(id):
    form = EditQuestionForm()
    question = Question.query.filter_by(id=id).first()
    if form.validate_on_submit():
        question.content = form.content.data
        question.question_type = form.question_type.data
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('teachers.questions_index'))

    form.content.data = question.content
    form.question_type.data = question.question_type

    return render_template('teacher/questions/edit.html', form=form)

# create cohort reports
@teacher.route('/assessments/<int:assessment_id>/report', methods=['GET', 'POST'])
@login_required
def cohort_report(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    questions = Question.query.filter_by(assessment_id=assessment_id).all()
    attempts = Attempt.query.filter_by(assessment_id=assessment_id).all()
    answers = Answer.query.filter_by(assessment_id=assessment_id).all()
    return render_template('teacher/reports/cohort/index.html', assessment=assessment, questions=questions, attempts=attempts, answers=answers)

# list of students
@teacher.route('/reports/', methods=['GET', 'POST'])
@login_required
def student_report():
    students = User.query.filter_by(role_id=1).all()
    return render_template('teacher/reports/student/index.html', students = students)

#view student report
@teacher.route('/reports/<int:student_id>', methods=['GET', 'POST'])
@login_required
def view_student_report(student_id):
    student = User.query.filter_by(id=student_id, role_id=1).first()
    if student is None:
        flash('Invalid student ID', 'error')
        return redirect(url_for('teachers.student_report'))
    
    attempts = Attempt.query.filter_by(created_by=student_id).all()
    return render_template('teacher/reports/student/show.html', student=student, attempts=attempts)

# view assessments that a student has taken
@teacher.route('/reports/<int:id>/assessments', methods=['GET', 'POST'])
@login_required
def view_student_assessments(id):
    student = User.query.filter_by(id=id, role_id=1).first()
    if student is None:
        flash('Invalid student ID', 'error')
        return redirect(url_for('teachers.student_report'))
    
    assessments = (db.session.query(Assessment)
                   .join(Attempt, Assessment.id == Attempt.assessment_id)
                   .filter(Attempt.created_by == student.id)
                   .distinct()
                   .all())

    return render_template('teacher/reports/student/list.html', student=student, assessments=assessments)

# view a student's attempt at an assessment
@teacher.route('/reports/<int:student_id>/assessments/<int:assessment_id>', methods=['GET', 'POST'])
@login_required
def view_student_assessment_report(student_id, assessment_id):
    student = User.query.filter_by(id=student_id, role_id=1).first()
    if student is None:
        flash('Invalid student ID', 'error')
        return redirect(url_for('teachers.student_report'))

    assessment = Assessment.query.get_or_404(assessment_id)
    questions = Question.query.filter_by(assessment_id=assessment_id).all()
    attempt = Attempt.query.filter_by(created_by=student_id, assessment_id=assessment_id).all()
    answers = Answer.query.filter_by(attempt_id=attempt.id).all()
    return render_template('teacher/reports/student/report.html', student=student, assessment=assessment, questions=questions, attempt=attempt, answers=answers)