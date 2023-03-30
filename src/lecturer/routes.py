from flask import Blueprint, render_template, redirect, url_for, flash
from flask import current_app
from flask_login import login_required
from src.lecturer.forms import CreateAssessmentForm, CreateQuestionForm
from src.models.assessment import Assessment
from src.models.question import Question
from src import db

lecturer = Blueprint('lecturer', __name__)

@lecturer.route("/lecturer")
@login_required
def home():
    return render_template('lecturer/home.html')

@lecturer.route('/lecturer/create_assessment', methods=['GET', 'POST'])
@login_required
def create_assessment():
    form = CreateAssessmentForm()
    if form.validate_on_submit():
        assessment = Assessment(title=form.title.data, description=form.description.data)
        db.session.add(assessment)
        db.session.commit()
        flash('Assessment created successfully!')
        return redirect(url_for('lecturer.home'))
    return render_template('lecturer/create_assessment.html', form=form)

@lecturer.route('/assessment/<int:assessment_id>/create_question', methods=['GET', 'POST'])
@login_required
def create_question(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    form = CreateQuestionForm()
    if form.validate_on_submit():
        question = Question(text=form.text.data, assessment_id=assessment.id)
        db.session.add(question)
        db.session.commit()
        
        flash('Question created successfully!')
        return redirect(url_for('lecturer.assessment_questions', assessment_id=assessment.id))
    return render_template('create_question.html', form=form, assessment=assessment)