from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.entry.forms import RegistrationForm, LoginForm
from src.models.user import User, Role
from src import db, bcrypt
from flask import current_app
from flask_login import login_user, current_user, logout_user

entry = Blueprint('entry', __name__)


@entry.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #checks if user exists and if password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            #redirects to the next page if it exists
            next_page = request.args.get('next')
        if current_user.is_authenticated:
            if user.role.name == 'Student':
                return redirect(url_for('student.home'))
            elif user.role.name == 'Lecturer':
                return redirect(url_for('lecturer.home'))
            flash(f'You have been logged in as a {current_user.role.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('student.home'))
        else:
            flash('Login Unsuccessful. Please check your username and password.', 'unsuccessful')
    return render_template('login.html', title='Login', form=form)


@entry.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if user.role.name == 'Student':
            return redirect(url_for('student.home'))
        elif user.role.name == 'Lecturer':
            return redirect(url_for('lecturer.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        role = Role.query.filter_by(name=form.role.data).first()
        if role is None:
            # If the role doesn't exist, create a new one
            role = Role(name=form.role.data)
            db.session.add(role)
        user.role = role
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you are now able to login', 'success')
        return redirect(url_for('entry.login'))
    return render_template('register.html', title='Register', form=form)


@entry.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('entry.login'))
