from flask import render_template, redirect, url_for, flash
from src.forms import RegistrationForm, LoginForm
from src import app

@app.route("/")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data:
            flash('You have been logged in!', 'alert-success')
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/home")
def home():
    return render_template('home.html')