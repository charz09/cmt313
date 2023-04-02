from flask import Blueprint, render_template, redirect, url_for, flash
from flask import current_app
from flask_login import login_required, current_user
from src.lecturer.forms import CreateAssessmentForm, CreateQuestionForm
from src.models.assessment import Assessment
from src.models.question import Question
from src import db

lecturer = Blueprint('lecturer', __name__)

@lecturer.route("/lecturer")
@login_required
def home():
    assessments = Assessment.query.filter_by(user_id=current_user.id).all()
    return render_template('lecturer/assessment/index.html', assessments = assessments)

#create assessments
@lecturer.route('/lecturer/create_assessment', methods=['GET', 'POST'])
@login_required
def create_assessment():
    form = CreateAssessmentForm()
    if form.validate_on_submit():
        assessment = Assessment(title=form.title.data, description=form.description.data, user_id=current_user.id)
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

#create questions
@lecturer.route('/lecturer/assessment/<int:assessment_id>/create_question', methods=['GET', 'POST'])
@login_required
def create_question(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    form = CreateQuestionForm()
    if form.validate_on_submit():
        question = Question(text=form.text.data, content=form.content.data, assessment_id=assessment.id)
        db.session.add(question)
        db.session.commit()
        
        flash('Question created successfully!')
        return redirect(url_for('lecturer.home', assessment_id=assessment.id))
    return render_template('lecturer/question/create.html', form=form, assessment=assessment)