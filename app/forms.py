from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, validators, HiddenField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required
from app import db
from app import models


class EmailOnly(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35)])


class LoginForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password')
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(Form):
    username = TextField('Username', [validators.Length(min=3, max=35)])
    email = TextField('E-mail Address', [validators.Email()])
    email_confirm = TextField('E-mail (confirm)', [Required(), validators.EqualTo('email', message='Must match %(other_label)s')])
    first_name = TextField('First Name', [validators.Length(min=2, max=35)])
    last_name = TextField('First Name', [validators.Length(min=2, max=35)])
    password = PasswordField('Password', [Required(), validators.Length(min=6)])
    password_confirm = PasswordField('Password (confirm)', [validators.EqualTo('password', message='Must match %(other_label)s')])


class PasswordReset(Form):
    activation_code = HiddenField('activation_code')
    password = PasswordField('Password', [Required(), validators.Length(min=6)])
    password_confirm = PasswordField('Password (confirm)', [validators.EqualTo('password', message='Must match %(other_label)s')])


class BeerStyleTypeForm(Form):
    name = TextField('Style Type Name', [validators.Length(min=3, max=35)])
    description = TextAreaField('Description')


class BeerStyleForm(Form):
    name = TextField('Style Name', [validators.Length(min=3, max=35)])
    description = TextAreaField('Description')
    #category = QuerySelectField('category', query_factory=lambda: db.session.query(Category), get_pk=lambda a: a.id, get_label=lambda a: a.name)
    style_type = QuerySelectField('category', query_factory=lambda: db.session.query(models.BeerStyleType), get_pk=lambda a: a.id, get_label=lambda a: a.name)
    #style_type = QuerySelectField('Type', query_factory=BeerStyleType.query.all)
    link_ratebeer = TextField('Link (www.ratebeer.com)', [validators.URL, validators.Length(min=10, max=255)])
    link_beeradvocate = TextField('Link (www.beeradvocate.com)', [validators.URL, validators.Length(min=10, max=255)])