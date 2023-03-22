from . import auth
from flask import render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired


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
                      ('student', 'Student'), ('teacher', 'Teacher')])
    submit = SubmitField('Sign Up')


@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        session['password'] = form.password.data
        return redirect(url_for('students.index'))
    return render_template('auth/login.html', form=form, username=session.get('username'), password=session.get('password'))


@auth.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        session['password'] = form.password.data
        session['confirm_password'] = form.confirm_password.data
        session['role'] = form.role.data
        return redirect(url_for('students.index'))
    return render_template('auth/register.html', form=form)


# @auth.route('/logout')
# def logout():
#     return render_template('auth/index.html')
