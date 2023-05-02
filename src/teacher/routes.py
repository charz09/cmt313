from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src import db
from ..models.assessment import Assessment
from ..models.question import Question
from ..models.choice import Choice
from ..models.user import User
from .forms import NewAssessmentForm, NewQuestionForm, EditAssessmentForm, EditQuestionForm
from . import teacher
from datetime import datetime

# protects the route against student access


@teacher.before_request
def check_user_is_teacher():
    if not current_user:
        return redirect(url_for('auth.login'))
    elif current_user.role.name == "Student":
        return redirect(url_for('students.index'))

# VIEW ASSESSMENTS


@teacher.route('/', methods=['GET'])
@teacher.route('/assessments', methods=['GET'])
@login_required
def assessments_index():
    # only return a users own assessments
    assessments = Assessment.query.filter_by(user_id=current_user.id)
    return render_template('teacher/assessments/summative/index.html', assessments=assessments)


# NEW ASSESSMENT
@teacher.route('/assessments/new', methods=['GET', 'POST'])
@login_required
def new_assessment():
    form = NewAssessmentForm()

    user_modules = current_user.modules
    choices = []
    for module in user_modules:
        choices.append((module.id, f"{module.code}: {module.name}"))
    form.module_id.choices = choices

    # pre populate the dates with right now.
    form.available_from.data = datetime.utcnow()
    form.available_to.data = datetime.utcnow()
    form.feedback_from.data = datetime.utcnow()

    if request.method == "POST":
        assessment = Assessment(name=form.name.data,
                                description=form.description.data,
                                module_id=form.module_id.data,
                                assessment_type=form.assessment_type.data,
                                user_id=current_user.id,
                                available_from=form.available_from.data,
                                available_to=form.available_to.data,
                                feedback_from=form.feedback_from.data
                                )
        db.session.add(assessment)
        db.session.commit()

        flash('Assessment Created Successfully!')
        return redirect(url_for('teachers.assessments_index'))

    return render_template('teacher/assessments/summative/new.html', form=form)


# SHOW + DELETE
@teacher.route('/assessments/<int:id>', methods=['GET', 'POST'])
@login_required
def show_assessment(id):
    if request.method == 'POST':
        assessment = Assessment.query.filter_by(id=id).first()
        db.session.delete(assessment)
        db.session.commit()
        flash('Assessment Deleted!')
        return redirect(url_for('teachers.assessments_index'))

    assessment = Assessment.query.filter_by(id=id).first()
    return render_template('teacher/assessments/summative/show.html', assessment=assessment, labels=["A", "B", "C", "D"])

# STATS


@teacher.route('/assessments/<int:id>/stats', methods=['GET'])
@login_required
def assessment_stats(id):
    assessment = Assessment.query.get(id)
    user_data = {}
    users = User.query.all()

    return render_template('teacher/assessments/summative/stats.html', assessment=assessment, users=users)


# EDIT ASSESSMENT
@teacher.route('/assessments/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_assessment(id):
    form = EditAssessmentForm()
    assessment = Assessment.query.first_or_404(id)

    user_modules = current_user.modules
    choices = []
    for module in user_modules:
        choices.append((module.id, f"{module.code}: {module.name}"))
    form.module_id.choices = choices

    if request.method == 'POST':
        assessment.name = form.name.data
        assessment.description = form.description.data
        assessment.module_id = form.module_id.data
        assessment.assessment_type = form.assessment_type.data

        assessment.available_from = form.available_from.data
        assessment.available_to = form.available_to.data
        assessment.feedback_from = form.feedback_from.data
        db.session.add(assessment)
        db.session.commit()
        flash('Assessment Updated Successfully!')
        return redirect(url_for('teachers.assessments_index'))

    form.name.data = assessment.name
    form.description.data = assessment.description
    form.module_id.data = assessment.module.id
    form.assessment_type.data = assessment.assessment_type
    form.available_from.data = assessment.available_from
    form.available_to.data = assessment.available_to
    form.feedback_from.data = assessment.feedback_from

    return render_template('teacher/assessments/summative/edit.html', form=form)


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

        return redirect(url_for('teachers.show_assessment', id=id))
    return render_template('teacher/questions/new.html', form=form)


# EDIT QUESTION
@teacher.route('/questions/<int:id>/edit', methods=['GET', 'POST'])
def edit_question(id):
    form = EditQuestionForm()
    question = Question.query.filter_by(id=id).first()
    assessment = question.assessment
    choices = question.choices
    if form.validate_on_submit():
        question.content = form.content.data
        question.question_type = form.question_type.data
        db.session.add(question)

        correct_choice = [
            c for c in choices if c.is_correct == True][0]
        correct_choice.content = form.correct_choice.data

        incorrect_choices = [c for c in choices if c.is_correct == False]
        incorrect_choices[0].content = form.incorrect_choice_1.data
        incorrect_choices[1].content = form.incorrect_choice_2.data
        incorrect_choices[2].content = form.incorrect_choice_3.data

        db.session.add(correct_choice)
        db.session.add(incorrect_choices[0])
        db.session.add(incorrect_choices[1])
        db.session.add(incorrect_choices[2])
        db.session.commit()

        return redirect(url_for('teachers.show_assessment', id=assessment.id))

    form.content.data = question.content
    form.question_type.data = question.question_type
    choices = question.choices
    form.correct_choice.data = [
        c for c in choices if c.is_correct == True][0].content
    incorrect_choices = [c for c in choices if c.is_correct == False]
    form.incorrect_choice_1.data = incorrect_choices[0].content
    form.incorrect_choice_2.data = incorrect_choices[1].content
    form.incorrect_choice_3.data = incorrect_choices[2].content

    return render_template('teacher/questions/edit.html', form=form)


# Delete QUESTION
@teacher.route('/questions/<int:id>/delete', methods=['POST'])
def delete_question(id):
    question = Question.query.filter_by(id=id).first()
    assessment = question.assessment
    assessment.number_of_questions -= 1
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('teachers.show_assessment', assessment=assessment, id=assessment.id))
