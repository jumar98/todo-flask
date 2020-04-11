from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Send')


class SignupForm(LoginForm):

    def __init__(self):
        super(LoginForm, self).__init__()


class TaskForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')


class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Delete')


class UpdateTaskForm(FlaskForm):
    submit = SubmitField('Edit')