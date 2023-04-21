from flask import Blueprint, render_template, redirect, url_for, flash
from flask import current_app
from flask_login import login_required, current_user
from src.lecturer.forms import CreateAssessmentForm, EditAssessmentForm, CreateQuestionForm
from src.models.user import User, Role
from src.models.assessment import Assessment
from src.models.question import Question,Choice
from src import db

lecturer = Blueprint('lecturer', __name__)

@lecturer.route("/lecturer")
@login_required
def home():
    assessments = Assessment.query.filter_by(user_id=current_user.id).all()
    return render_template('lecturer/assessment/index.html', assessments = assessments)

# create assessment
@lecturer.route('/lecturer/create_assessment', methods=['GET', 'POST'])
@login_required
def create_assessment():
    form = CreateAssessmentForm()
    if form.validate_on_submit():
        assessment = Assessment(title=form.title.data, description=form.description.data, assessment_type=form.assessment_type.data, user_id=current_user.id)
        db.session.add(assessment)
        db.session.commit()
        flash('Assessment created successfully!')
        return redirect(url_for('lecturer.home'))
    return render_template('lecturer/assessment/create.html', form=form)


#view assessment
@lecturer.route('/lecturer/assessment/<int:assessment_id>', methods=['GET', 'POST'])
@login_required
def view_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    questions = Question.query.filter_by(assessment_id=assessment.id).all()
    return render_template('lecturer/assessment/view.html', assessment=assessment, questions=questions)

# edit assessment
@lecturer.route('/lecturer/assessment/<int:assessment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_assessment(assessment_id):
    # edit assessment
    assessment = Assessment.query.get_or_404(assessment_id)
    form = EditAssessmentForm()
    if form.validate_on_submit():
        assessment.title = form.title.data
        assessment.description = form.description.data
        assessment.assessment_type = form.assessment_type.data
        db.session.add(assessment)
        db.session.commit()
        flash('Assessment updated successfully!')
        return redirect(url_for('lecturer.home'))

    # load assessment data into form
    form.title.data = assessment.title
    form.description.data = assessment.description
    form.assessment_type.data = assessment.assessment_type
    return render_template('lecturer/assessment/edit.html', form=form, assessment=assessment)


#delete assessment
@lecturer.route('/lecturer/assessment/<int:assessment_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    db.session.delete(assessment)
    db.session.commit()
    flash('Assessment deleted successfully!')
    return redirect(url_for('lecturer.home'))

@lecturer.route('/lecturer/assessment/<int:assessment_id>/create_question', methods=['GET', 'POST'])
@login_required
def create_question(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    form = CreateQuestionForm()
    if form.validate_on_submit():
        question = Question(
            text=form.question.data, 
            question_type=form.question_type.data, 
            answer=form.answer.data, 
            assessment_id=assessment.id
        )
        db.session.add(question)
        
        if form.question_type.data == "multiple_choice":
            for i in range(1, 4):
                choice_text = getattr(form, f"choice_{i}").data
                is_correct = (i == int(form.answer.data))
                choice = Choice(text=choice_text, is_correct=is_correct, question=question)
                db.session.add(choice)
        
        db.session.commit()
        flash('Question created successfully!')
        return redirect(url_for('lecturer.home', assessment_id=assessment.id))
    return render_template('lecturer/question/create.html', form=form, assessment=assessment)

# create cohort reports
@lecturer.route('/lecturer/assessment/<int:assessment_id>/cohort_report', methods=['GET', 'POST'])
@login_required
def cohort_report(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    questions = Question.query.filter_by(assessment_id=assessment_id).all()
    return render_template('lecturer/report/cohort.html')

# list of students
@lecturer.route('/lecturer/student_report', methods=['GET', 'POST'])
@login_required
def student_report():
    students = User.query.filter_by(role_id=2).all()
    return render_template('lecturer/report/student.html', students = students)