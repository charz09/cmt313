from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from src import db
from ..models.user import User
from ..models.assessment import Assessment
from ..models.attempt import Attempt
from ..models.question import Question
from ..models.choice import Choice
from ..models.answer import Answer
from ..models.session import UserSession
from .forms import NewAssessmentForm, NewQuestionForm, EditAssessmentForm, EditQuestionForm
from . import teacher
from datetime import datetime, timedelta
import numpy as np
import calendar


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
@teacher.route('/reports/cohort', methods=['GET', 'POST'])
@login_required
def cohort_report():

# set default time period
    time_period = 'daily'

    # calculate start and end time based on time period
    end_time = datetime.now()
    if time_period == 'daily':
        start_time = end_time - timedelta(days=1)
    elif time_period == 'weekly':
        start_time = end_time - timedelta(weeks=1)
    elif time_period == 'monthly':
        start_time = end_time - timedelta(days=30)

    # query user sessions
    sessions = UserSession.query.filter(
        UserSession.start_time >= start_time,
        UserSession.end_time <= end_time
    ).all()

    # calculate number of users
    user_counts = {}
    total_duration = 0
    for session in sessions:
        session_date = session.start_time.date()
        if session_date not in user_counts:
            user_counts[session_date] = set()
        user_counts[session_date].add(session.user_id)
        user_counts[session_date].add(session.user_id)
    total_duration += (session.end_time - session.start_time).total_seconds()

    # calculate daily, weekly, and monthly averages
    if time_period == 'daily':
        num_days = 1
    elif time_period == 'weekly':
        num_days = 7
    elif time_period == 'monthly':
        num_days = 30

    num_users = sum(len(user_counts[date]) for date in user_counts)
    num_periods = len(user_counts)
    if num_periods > 0:
        avg_users = int(num_users / num_periods)
        avg_users_period = int(num_users / num_periods * num_days)
        avg_duration = int(total_duration / len(sessions))
    else:
        avg_users = 0
        avg_users_period = 0
        avg_duration = 0

    # create a dictionary of average users for each time period
    engagement_dict = {
        'daily': avg_users_period,
        'weekly': int(num_users / (num_periods / 7)),
        'monthly': int(num_users / (num_periods / 30)),
        'overall': avg_users
    }
    
    assessments = Assessment.query.all()
    # get selected assessment_id from form
    assessment_id = request.form.get('assessment_id')
    if assessment_id:
        # get the chosen assessment
        chosen_assessment = Assessment.query.get(assessment_id)
        # get the attempts for the chosen assessment
        attempts = chosen_assessment.attempts
        
        # calculate the average time taken for all assessments overall
        total_time_taken = sum([(attempt.end_time - attempt.created_on).total_seconds() for attempt in attempts])
        average_time_taken_seconds = total_time_taken / len(attempts) if attempts else 0
        average_time_taken = '{:02d}:{:02d}'.format(int(average_time_taken_seconds // 60), int(average_time_taken_seconds % 60))
        
        #calculate completeion rate
        num_students_attempted = len(set([attempt.created_by for attempt in attempts]))
        num_students_eligible = len(User.query.filter_by(role_id=1).all())
        completion_rate = f"{num_students_attempted/num_students_eligible:.0%}"

        # calculate the number of times each question was answered correctly and incorrectly for each assessment
        questions = chosen_assessment.questions
        question_results = []
        for question in questions:
            num_correct = 0
            num_incorrect = 0
            for attempt in attempts:
                answer = Answer.query.filter_by(
                    attempt_id=attempt.id, question_id=question.id).first()
                if answer and answer.is_correct:
                    num_correct += 1
                elif answer:
                    num_incorrect += 1
            question_results.append(
                {'question': question, 'num_correct': num_correct, 'num_incorrect': num_incorrect})

        # calculate the statistics for the chosen assessment
        total_num_of_attempts = len(attempts)
        total_num_of_students_passed = len(
            [attempt for attempt in attempts if attempt.user_score >= attempt.total_score * 0.5])
        average_score = sum([attempt.user_score for attempt in attempts]
                            )/len(attempts) * 10 if attempts else 0
        average_attempts = len(
            attempts)/len(set([attempt.id for attempt in attempts])) if attempts else 0
        
        # get data for each student
        students = User.query.filter_by(role_id=1).all()
        student_data = []
        for student in students:
            student_attempts = Attempt.query.filter_by(created_by=student.id, assessment_id=assessment_id).all()
            if student_attempts:
                student_num_of_attempts = len(student_attempts)
                student_num_of_correct_attempts = len(
                    [attempt for attempt in student_attempts if attempt.user_score >= attempt.total_score * 0.5])
                student_average_score = sum(
                    [attempt.user_score for attempt in student_attempts])/student_num_of_attempts * 10
                # calculate the average time taken for the chosen assessment
                student_time_taken = sum([(attempt.end_time - attempt.created_on).total_seconds() for attempt in student_attempts])
                student_average_time_taken_seconds = student_time_taken / len(student_attempts) if student_attempts else 0
                student_average_time_taken = '{:02d}:{:02d}'.format(int(student_average_time_taken_seconds // 60), int(student_average_time_taken_seconds % 60))
                print(student_average_time_taken)
                student_data.append({'id': student.id, 'name': student.username, 'num_of_attempts': student_num_of_attempts,
                                     'num_of_correct_attempts': student_num_of_correct_attempts, 'average_score': student_average_score, 'average_time_taken': student_average_time_taken})

        return render_template('teacher/reports/cohort/index.html', students=students, student_data=student_data, chosen_assessment=chosen_assessment,
                               assessments=assessments, average_score=average_score,
                               average_attempts=average_attempts,
                               total_num_of_attempts=total_num_of_attempts,
                               total_num_of_students_passed=total_num_of_students_passed, question_results=question_results, average_time_taken=average_time_taken, completion_rate=completion_rate, time_period=time_period, engagement_dict=engagement_dict)
        
    else:
        return render_template('teacher/reports/cohort/index.html', assessments=assessments, time_period=time_period, engagement_dict=engagement_dict)


# list of students
@teacher.route('/reports/student', methods=['GET', 'POST'])
@login_required
def student_report():
    page = request.args.get('page', 1, type=int)
    students = User.query.filter_by(role_id=1).paginate(page=page, per_page=5)
    return render_template('teacher/reports/student/index.html', students=students)


@teacher.route('/reports/student/<int:id>', methods=['GET', 'POST'])
@login_required
def view_student_report(id):
    student = User.query.filter_by(id=id, role_id=1).first()
    if student is None:
        flash('Invalid student ID', 'error')
        return redirect(url_for('teachers.student_report'))

    attempts = Attempt.query.filter_by(created_by=id).all()
    overall_assessment_scores = {}
    overall_assessment_attempts = {}
    overall_assessment_passed = {}
    for attempt in attempts:
        assessment_id = attempt.assessment_id
        if assessment_id not in overall_assessment_scores:
            overall_assessment_scores[assessment_id] = []
            overall_assessment_attempts[assessment_id] = []
            overall_assessment_passed[assessment_id] = []
        if attempt.total_score is not None:
            user_score_percentage = (
                attempt.user_score / attempt.total_score) * 100
            if user_score_percentage >= 60:
                overall_assessment_passed[assessment_id].append(attempt)
            overall_assessment_scores[assessment_id].append(user_score_percentage)
            overall_assessment_attempts[assessment_id].append(attempt)

    assessment_data = []
    total_assessments = len(Assessment.query.all())
    attempted_assessments = 0
    for assessment_id in overall_assessment_scores.keys():
        total_attempts = len(overall_assessment_attempts[assessment_id])
        total_passed = len(overall_assessment_passed[assessment_id])
        if total_attempts > 0:
            overall_avg_score = sum([score for score in overall_assessment_scores[assessment_id]
                            if score is not None]) / total_attempts
            avg_attempts_overall = total_attempts / \
                len(set(
                    [attempt.assessment_id for attempt in overall_assessment_attempts[assessment_id]]))
            scores = [
                score for score in overall_assessment_scores[assessment_id] if score is not None]
            assessment_data.append({
                'name': Assessment.query.filter_by(id=assessment_id).first().name,
                'avg_score': overall_avg_score,
                'avg_attempts': avg_attempts_overall,
                'total_attempts': total_attempts,
                'total_passed': total_passed,
                'class_avg_score': get_class_avg_score(assessment_id, student),
            })
            attempted_assessments += 1

    completion_rate = (attempted_assessments / total_assessments) * \
        100 if total_assessments > 0 else 0

    assessment_avg_scores = {}
    for assessment in assessment_data:
        assessment_avg_scores[assessment['name']] = assessment['avg_score']
    
    # get unique assessments attempted by the student
    assessments = []
    for attempt in attempts:
        if attempt.assessment not in assessments:
            assessments.append(attempt.assessment)

    get_assessment_id = request.form.get('assessment_id')
    if get_assessment_id:
        chosen_assessment = Assessment.query.get(get_assessment_id)
        attempts = chosen_assessment.attempts
        questions = chosen_assessment.questions
        
        #new code below
        # Get assessment data for the student
        student_attempts = Attempt.query.filter_by(
            created_by=id, assessment_id=get_assessment_id).all()
        assessment_scores = []
        assessment_passed = []
        for attempt in student_attempts:
            if attempt.total_score is not None:
                student_score_percentage = attempt.user_score / attempt.total_score
                if student_score_percentage >= 0.6:
                    assessment_passed.append(attempt)
                assessment_scores.append(attempt.user_score)

        # Calculate the average score for this assessment for this student, as well as other relevant data
        student_avg_score = (sum(assessment_scores) / len(assessment_scores)
                    ) * 10 if len(assessment_scores) > 0 else 0
        student_avg_attempts = len(attempts) / \
            len(set([attempt.created_by for attempt in attempts]))
        student_total_attempts = len(attempts)
        student_total_passed = len(assessment_passed)

    # Calculate the number of times each question was answered correctly and incorrectly for the selected student's attempts
        question_results = []
        for question in questions:
            num_correct = 0
            num_incorrect = 0
            for attempt in student_attempts:
                answer = Answer.query.filter_by(
                    attempt_id=attempt.id, question_id=question.id).first()
                if answer and answer.is_correct:
                    num_correct += 1
                elif answer:
                    num_incorrect += 1
            question_results.append(
                {'question': question, 'num_correct': num_correct, 'num_incorrect': num_incorrect})

        # Create a dictionary of assessment data to be passed to the template
        student_assessment_data = {
            'name': chosen_assessment.name,
            'avg_score': student_avg_score,
            'avg_attempts': student_avg_attempts,
            'total_attempts': student_total_attempts,
            'total_passed': student_total_passed,
            'class_avg_score': get_class_avg_score(get_assessment_id, student)
        }

        return render_template('teacher/reports/student/show.html', student=student, assessment_data=assessment_data, assessment_avg_scores=assessment_avg_scores, completion_rate=completion_rate, student_assessment_data=[student_assessment_data], question_results=question_results, assessments=assessments, chosen_assessment=chosen_assessment, questions=questions)
    else:
        return render_template('teacher/reports/student/show.html', student=student, assessment_data=assessment_data, assessment_avg_scores=assessment_avg_scores, completion_rate=completion_rate, assessments=assessments)


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