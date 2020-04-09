from flask import (request, make_response, redirect,
                   render_template, session)
import unittest
from app import create_app

app = create_app()

tasks = ['Buy coffe', 'Do homework', 'Go shopping']


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


@app.route('/hello_world', methods=['GET'])
def hello_world():
    user_address = session.get('user_address')
    username = session.get('username')
    context = {
        'user_address': user_address,
        'tasks': tasks,
        'username': username
    }

    return render_template('hello.html', **context)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)
