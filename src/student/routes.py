from flask import render_template, redirect, url_for, request, flash
from . import student
from src import db
import datetime
from ..models.user import User
from ..models.assessment import Assessment
from ..models.attempt import Attempt
from ..models.question import Question
from ..models.choice import Choice
from ..models.answer import Answer
from flask_login import login_required, current_user
from .forms import NewAttemptForm
from wtforms import StringField, RadioField
import numpy as np
# from src import db
# from wtforms.validators import DataRequired


# View all assessment attempts
@student.route('/')
@login_required
def index():
    assessments = Assessment.query.all()
    return render_template('student/attempts/index.html', assessments=assessments)


# Create new Assessment attempt
@student.route('/assessments/<int:id>/attempt/new', methods=['GET', 'POST'])
@login_required
def new_attempt(id):
    assessment = Assessment.query.get(id)

    # Build a form dynamically, for whatever questions are in the assessment.
    for i, question in enumerate(assessment.questions):
        if question.question_type == "Multiple Choice":
            # Build a tuple of choices for the radio button.
            choices = []
            for choice in question.choices:
                choices.append((choice.content, choice.content))
                # set the attribute on the form under the value "question_?"
                setattr(NewAttemptForm, f"question_{i}", RadioField(
                    question.content,  choices=choices))
        else:
            # set the attribute on the form under the value "question_?"
            setattr(NewAttemptForm, f"question_{i}", StringField(
                question.content, render_kw={"data-question-id": f"{question.id}"}))

    form = NewAttemptForm()

    # on_validate was not working, so switeched to:
    if request.method == "POST":
        attempt = Attempt.create(assessment.id,
                                 current_user.id)
        attempt.end_time = datetime.datetime.now()

        # Creates the Answer objects and stores the users answer, the correct answer etc..
        for i, question in enumerate(assessment.questions):
            # Search the questions choices for the correct choice
            correct_choice = [
                choice for choice in question.choices if choice.is_correct == True][0].content

            # get the users answer dynamically from the form object
            user_choice = getattr(form, f"question_{i}").data

            if user_choice == correct_choice:
                Answer.create(
                    user_choice, True, correct_choice, attempt.id, question.id)
            else:
                Answer.create(
                    user_choice, False, correct_choice, attempt.id, question.id)

        return redirect(url_for('students.results', id=attempt.id))

    return render_template('student/attempts/new.html', form=form)


# See the results of an attempt
@student.route('/attempts/<int:id>/results', methods=['GET'])
@login_required
def results(id):
    attempt = Attempt.query.get(id)
    return render_template('student/attempts/results.html', attempt=attempt)

@student.route('/progress/<int:id>', methods=['GET', 'POST'])
@login_required
def view_report(id):
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
