from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, validators
from wtforms.validators import Required

class LoginForm(Form):
	
   email = TextField('Email Address', [validators.Length(min=6, max=35)])
   password = PasswordField('Password')
   remember_me = BooleanField('remember_me', default = False)

class RegisterForm(Form):
	
   username = TextField('Username', [validators.Length(min=3, max=35)])
   email = TextField('E-mail Address', [validators.Email()])
   email_confirm = TextField('E-mail (confirm)', [Required(), validators.EqualTo('email', message='Must match %(other_label)s')])
   firstname = TextField('First Name', [validators.Length(min=2, max=35)])
   lastname = TextField('First Name', [validators.Length(min=2, max=35)])
   password = PasswordField('Password', [Required(), validators.Length(min=6)])
   password_confirm = PasswordField('Password (confirm)', [validators.EqualTo('password', message='Must match %(other_label)s')])
