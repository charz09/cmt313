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

# create cohort report for each assessment
@teacher.route('/assessments/<int:id>/report', methods=['GET', 'POST'])
@login_required
def cohort_report(id):
    assessment = Assessment.query.get_or_404(id)
    questions = Question.query.filter_by(assessment_id=id).all()
    attempts = Attempt.query.filter_by(assessment_id=id).all()
    answers = Answer.query.filter_by(attempt_id=id).all()
    return render_template('teacher/reports/cohort/index.html', assessment=assessment, questions=questions, attempts=attempts, answers=answers)

# list of students
@teacher.route('/reports/', methods=['GET', 'POST'])
@login_required
def student_report():
    students = User.query.filter_by(role_id=1).all()
    return render_template('teacher/reports/student/index.html', students = students)

#view student report
@teacher.route('/reports/<int:id>', methods=['GET', 'POST'])
@login_required
def view_student_report(id):
    student = User.query.filter_by(id=id, role_id=1).first()
    if student is None:
        flash('Invalid student ID', 'error')
        return redirect(url_for('teachers.student_report'))

    attempts = Attempt.query.filter_by(created_by=id).all()
    assessment_scores = {}
    assessment_attempts = {}
    assessment_passed = {}
    for attempt in attempts:
        assessment_id = attempt.assessment_id
        if assessment_id not in assessment_scores:
            assessment_scores[assessment_id] = []
            assessment_attempts[assessment_id] = []
            assessment_passed[assessment_id] = []
        if attempt.total_score is not None:
            user_score_percentage = (attempt.user_score / attempt.total_score) * 100
            if user_score_percentage >= 60:
                assessment_passed[assessment_id].append(attempt)
            assessment_scores[assessment_id].append(user_score_percentage)
            assessment_attempts[assessment_id].append(attempt)

    assessment_data = []
    for assessment_id in assessment_scores.keys():
        total_attempts = len(assessment_attempts[assessment_id])
        total_passed = len(assessment_passed[assessment_id])
        if total_attempts > 0:
            avg_score = sum([score for score in assessment_scores[assessment_id] if score is not None]) / total_attempts
            avg_attempts = total_attempts / len(set([attempt.assessment_id for attempt in assessment_attempts[assessment_id]]))
            scores = [score for score in assessment_scores[assessment_id] if score is not None]
            assessment_data.append({
                'name': Assessment.query.filter_by(id=assessment_id).first().name,
                'avg_score': avg_score,
                'avg_attempts': avg_attempts,
                'total_attempts': total_attempts,
                'total_passed': total_passed,
                'class_avg_score': get_class_avg_score(assessment_id, student),
            })
    assessment_avg_scores = {}
    for assessment in assessment_data:
        assessment_avg_scores[assessment['name']] = assessment['avg_score']

    return render_template('teacher/reports/student/show.html', student=student, assessment_data=assessment_data, assessment_avg_scores=assessment_avg_scores)


def get_class_avg_score(assessment_id, student):
    attempts = Attempt.query.filter_by(assessment_id=assessment_id).all()
    total_scores = 0
    total_students = 0
    for attempt in attempts:
        if attempt.created_by != student.id:
            if attempt.user_score is not None:  # only include attempts with non-None user_score
                total_scores += attempt.user_score
                total_students += 1
    if total_students > 0:
        avg_score = total_scores / total_students
        return round(avg_score * 10, 2)
    else:
        return 0

# view a list of assessments that a student has taken
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

@teacher.route('/reports/<int:student_id>/assessments/<int:assessment_id>', methods=['GET', 'POST'])
@login_required
def view_student_assessment_report(student_id, assessment_id):
    # Query the student with the given ID and ensure that they have the role ID of 1 (i.e., they are a student)
    student = User.query.filter_by(id=student_id, role_id=1).first()
    if student is None:
        # If the student cannot be found, flash an error message and redirect to the teacher's student report page
        flash('Invalid student ID', 'error')
        return redirect(url_for('teachers.student_report'))

    # Query the assessment with the given ID and get all questions associated with it
    assessment = Assessment.query.get_or_404(assessment_id)
    questions = Question.query.filter_by(assessment_id=assessment_id).all()

    # Get the attempt for this student on this assessment and all answers associated with it
    attempt = Attempt.query.filter_by(created_by=student_id, assessment_id=assessment_id).first()
    answers = Answer.query.filter_by(attempt_id=attempt.id).all()

    # Get assessment data for the student
    attempts = Attempt.query.filter_by(created_by=student_id, assessment_id=assessment_id).all()
    assessment_scores = []
    assessment_passed = []
    for attempt in attempts:
        if attempt.total_score is not None:
            user_score_percentage = attempt.user_score / attempt.total_score
            if user_score_percentage >= 0.6:
                assessment_passed.append(attempt)
            assessment_scores.append(attempt.user_score)

    # Calculate the average score for this assessment for this student, as well as other relevant data
    avg_score = (sum(assessment_scores) / len(assessment_scores)) * 10 if len(assessment_scores) > 0 else 0
    avg_attempts = len(attempts) / len(set([attempt.created_by for attempt in attempts]))
    total_attempts = len(attempts)
    total_passed = len(assessment_passed)
    class_avg_score = get_class_avg_score(assessment_id, student)

    # Create a dictionary of assessment data to be passed to the template
    assessment_data = {
        'name': assessment.name,
        'avg_score': avg_score,
        'avg_attempts': avg_attempts,
        'total_attempts': total_attempts,
        'total_passed': total_passed,
        'class_avg_score': class_avg_score,
    }

    # Render the template for the assessment report, passing in the relevant data
    return render_template('teacher/reports/student/assessment.html', student=student, assessment=assessment, questions=questions, attempt=attempt, answers=answers, assessment_data=[assessment_data])