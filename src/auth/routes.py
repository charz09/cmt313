from flask import render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from . import auth


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        session['username'] = form.username.data
        print(form.password.data)
        session['password'] = form.password.data
        return redirect(url_for('students.index'))
    return render_template('auth/login.html', form=form, username=session.get('username'), password=session.get('password'))


@auth.route('/register')
def register():
    return render_template('auth/register.html')


# @auth.route('/logout')
# def logout():
#     return render_template('auth/index.html')
