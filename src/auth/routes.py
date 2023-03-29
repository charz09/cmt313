from flask_login import logout_user, login_required, login_user
from . import auth  # auth is the current blueprint
from ..models.user import User
from ..models.role import Role
from flask import render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired
from src import db


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    role = RadioField('Role', validators=[DataRequired()], choices=[
                      ('Student', 'Student'), ('Teacher', 'Teacher')])
    submit = SubmitField('Sign Up')


@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            if user.role.name == "Student":
                return redirect(url_for('students.assessments_index'))
            else:
                return redirect(url_for('teachers.assessments_index'))

    return render_template('auth/login.html', form=form, username=session.get('username'), password=session.get('password'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() == None:
            user = User(username=form.username.data,
                        password=form.password.data)
            user.role_id = Role.query.filter_by(
                name=form.role.data).first().id
            db.session.add(user)
            db.session.commit()
            login_user(user)
            if user.role.name == "Student":
                return redirect(url_for('students.index'))
            else:
                return redirect(url_for('teachers.assessments_index'))

    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
