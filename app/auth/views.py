from . import auth
from app.forms import LoginForm
from flask import render_template, session, redirect, flash, url_for
from app.firestore_service import get_user
from app.models import UserModel, User
from flask_login import login_user


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
