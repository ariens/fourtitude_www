from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, validators, HiddenField
from wtforms.validators import Required


class EmailOnlyForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35)])


class LoginForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password')
    remember_me = BooleanField('remember_me', default=False)


class ConfirmForm(Form):
    pass


class RegisterForm(Form):
    username = TextField('Username', [validators.Length(min=3, max=35)])
    email = TextField('E-mail Address', [validators.Email()])
    email_confirm = TextField(
        'E-mail (confirm)', [Required(), validators.EqualTo('email', message='Must match %(other_label)s')])
    first_name = TextField('First Name', [validators.Length(min=2, max=35)])
    last_name = TextField('First Name', [validators.Length(min=2, max=35)])
    password = PasswordField('Password', [Required(), validators.Length(min=6)])
    password_confirm = PasswordField(
        'Password (confirm)', [validators.EqualTo('password', message='Must match %(other_label)s')])


class PasswordResetForm(Form):
    activation_code = HiddenField('activation_code')
    password = PasswordField('Password', [Required(), validators.Length(min=6)])
    password_confirm = PasswordField(
        'Password (confirm)', [validators.EqualTo('password', message='Must match %(other_label)s')])