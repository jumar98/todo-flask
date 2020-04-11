from . import auth
from app.forms import LoginForm, SignupForm
from flask import render_template, redirect, flash, url_for
from app.firestore_service import get_user, create_user
from app.models import UserModel, User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user_doc = get_user(username)
        if user_doc.to_dict():
            password_db = user_doc.to_dict()['password']
            if password == password_db:
                user_data = User(username, password)
                user = UserModel(user_data)
                login_user(user)
                flash('Welcome, again!.')
                redirect(url_for('hello_world'))
            else:
                flash('The information does not match.')
        else:
            flash('This user does not exists in our database')
        return redirect(url_for('index'))
    return render_template('login.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Good bye, Come back soon!.')
    return redirect(url_for('auth.login'))


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form
    }
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        user_doc = get_user(username)
        if not user_doc.to_dict():
            password_hash = generate_password_hash(password)
            user_data = User(username, password_hash)
            create_user(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('User registered with success')
            return redirect(url_for('hello_world'))
        else:
            flash('This usermane already exists!.')
    return render_template('signup.html', **context)
