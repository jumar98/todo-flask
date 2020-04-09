from flask import (Flask, request, make_response, redirect, url_for,
                   render_template, session, flash)
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = '1234567'

tasks = ['Buy coffe', 'Do homework', 'Go shopping']


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Send')


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.route('/')
def index():
    user_address = request.remote_addr
    response = make_response(redirect('/hello_world'))
    session['user_address'] = user_address
    return response


@app.route('/hello_world', methods=['GET', 'POST'])
def hello_world():
    form = LoginForm()
    user_address = session.get('user_address')
    username = session.get('username')
    context = {
        'user_address': user_address,
        'tasks': tasks,
        'form': form,
        'username': username
    }
    if form.validate_on_submit():
        username = form.username.data
        session['username'] = username
        flash('Username registered with success.')
        return redirect(url_for('index'))
    return render_template('hello.html', **context)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)
