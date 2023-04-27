from bs4 import Comment
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from src import db
from src.student.forms import CommentForm
from ..models.user import User
from ..models.assessment import Assessment
from ..models.attempt import Attempt
from ..models.question import Question
from ..models.choice import Choice
from ..models.answer import Answer
from ..models.feedback import Feedback
from .comments import comments
from .forms import NewAssessmentForm, NewQuestionForm, EditAssessmentForm, EditQuestionForm, FeedbackForm
from . import teacher

comments = Blueprint('comments', __name__)

# Added code for the teacher:
# teacher = Blueprint('teacher', __name__, url_prefix='/teacher')

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

# view a student comment after submission

@teacher.route('/teacher/assessments/<int:assessment_id>/new_comment', methods=['GET', 'POST'])
def new_comment(assessment_id):
    if request.method == 'POST':
        # process the form data and save the comment
        comment_text = request.form['comment_text']
        # save the comment to the database with the corresponding assessment_id
        # ...
        return redirect(url_for('teacher.view_assessment', assessment_id=assessment_id))
    else:
        # render the form for adding a new comment
        return render_template('new_comment.html', assessment_id=assessment_id)

@teacher.route('/reports/<int:assessment_id>/feedback', methods=['GET', 'POST'])
@login_required
def feedback(assessment_id):
    assessment = Assessment.query.get(assessment_id)
    feedbacks = Feedback.query.filter_by(assessment_id=assessment_id).all()
    return render_template('teacher/reports/feedback.html', assessment=assessment, feedbacks=feedbacks)



@teacher.route('/assessment/<int:assessment_id>/questions/<int:question_id>/comments', methods=['GET', 'POST'])
@login_required
def question_comments(assessment_id, question_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    question = Question.query.get_or_404(question_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, question_id=question_id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('question_comments', assessment_id=assessment_id, question_id=question_id))
    comments = question.comments.order_by(Comment.timestamp.asc())
    return render_template('question_comments.html', assessment=assessment, question=question, form=form, comments=comments)

@teacher.route('/reports/<int:attempt_id>/assessments/feedback', methods=['GET', 'POST'])
@login_required
def view_feedback(attempt_id):
    attempt = Attempt.query.get_or_404(attempt_id)
    assessment = attempt.assessment
    question = attempt.question
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, question_id=question.id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('teacher.view_feedback', attempt_id=attempt_id))
    comments = question.comments.order_by(Comment.timestamp.asc())
    has_feedback = Feedback.query.filter_by(student_id=attempt.student_id).first() is not None
    if not has_feedback:
        flash('No feedback submitted.', 'warning')
        return redirect(url_for('teacher.view_assessment', id=assessment.id))
    return render_template('feedback.html', attempt=attempt, question=question, form=form, comments=comments, has_feedback=has_feedback)
