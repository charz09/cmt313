from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.entry.forms import RegistrationForm, LoginForm
from src.models.user import User, Role
from src import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

entry = Blueprint('entry', __name__)

@entry.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('student.home'))
        else:
            flash('Login Unsuccessful. Please check your username and password.', 'unsuccessful')
    return render_template('login.html', title='Login', form=form)

@entry.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('student.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you are now able to login', 'success')
        return redirect(url_for('entry.login'))
    return render_template('register.html', title='Register', form=form)

@entry.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('entry.login'))