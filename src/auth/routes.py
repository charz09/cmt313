
from flask_login import logout_user, login_required, login_user, current_user
from . import auth  # auth is the current blueprint
from ..models.user import User
from ..models.role import Role
from .forms import LoginForm, RegisterForm, EditProfileForm
from flask import render_template, session, redirect, url_for, flash, request
from src import db


@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)

        if current_user.is_authenticated:
            if user.role.name == "Student":
                return redirect(url_for('students.index'))
            else:
                return redirect(url_for('teachers.assessments_index'))
            flash(
                f'You have been logged in as a {current_user.role.name}!', 'success')
        else:
            flash(
                'Login Unsuccessful. Please check your username and password.', 'unsuccessful')
    return render_template('auth/login.html', form=form, username=session.get('username'), password=session.get('password'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if user.role.name == 'Student':
            return redirect(url_for('student.home'))
        elif user.role.name == 'Lecturer':
            return redirect(url_for('lecturer.home'))

    form = RegisterForm()
    if form.validate_on_submit():
        # check if user already exists
        user = User(username=form.username.data,
                    password=form.password.data)
        user.role_id = Role.query.filter_by(
            name=form.role.data).first().id
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Your account has been created, you are now able to login', 'success')

        if user.role.name == "Student":
            return redirect(url_for('students.index'))
        else:
            return redirect(url_for('teachers.assessments_index'))

    return render_template('auth/register.html', form=form)


@auth.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('auth/user.html', user=user)

@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('auth.edit_profile'))
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
    return render_template('auth/edit_profile.html', title='Edit Profile',
                           form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
