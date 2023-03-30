from flask import Blueprint, render_template, redirect, url_for, flash
from flask import current_app
from flask_login import login_required
from src.lecturer.forms import AssessmentForm
from src.models.assessment import Assessment
from src import db

lecturer = Blueprint('lecturer', __name__)

@lecturer.route("/lecturer")
@login_required
def home():
    return render_template('lecturer/home.html')

@lecturer.route('/lecturer/create_assessment', methods=['GET', 'POST'])
@login_required
def create_assessment():
    form = AssessmentForm()
    if form.validate_on_submit():
        assessment = Assessment(title=form.title.data, description=form.description.data)
        db.session.add(assessment)
        db.session.commit()
        flash('Assessment created successfully!')
        return redirect(url_for('lecturer.home'))
    return render_template('lecturer/create.html', form=form)