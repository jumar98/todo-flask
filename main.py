from flask import (request, make_response, redirect,
                   render_template, url_for, session, flash)
import unittest
from app import create_app
from app.firestore_service import delete_task, get_tasks, create_task, update_task
from flask_login import login_required, current_user
from app.forms import UpdateTaskForm, TaskForm, DeleteTaskForm

app = create_app()


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
@login_required
def hello_world():
    task_form = TaskForm()
    user_address = session.get('user_address')
    username = current_user.id
    context = {
        'user_address': user_address,
        'tasks': get_tasks(username),
        'username': username,
        'task_form': task_form,
        'delete_task_form': DeleteTaskForm(),
        'update_task_form': UpdateTaskForm()
    }
    if task_form.validate_on_submit():
        create_task(username, task_form.description.data)
        flash('Task created with success.')
        return redirect(url_for('hello_world'))
    return render_template('hello.html', **context)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


@app.route('/tasks/delete/<task_id>', methods=['POST'])
def delete(task_id):
    user_id = current_user.id
    delete_task(user_id, task_id)
    return redirect(url_for('hello_world'))


@app.route('/tasks/update/<task_id>/<int:done>', methods=['POST'])
def update(task_id, done):
    user_id = current_user.id
    update_task(user_id, task_id, done)
    return redirect(url_for('hello_world'))
