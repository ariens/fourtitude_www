from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, validators, HiddenField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required
from fourtitude import db
from fourtitude import models


class EmailOnly(Form):
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


class PasswordReset(Form):
    activation_code = HiddenField('activation_code')
    password = PasswordField('Password', [Required(), validators.Length(min=6)])
    password_confirm = PasswordField(
        'Password (confirm)', [validators.EqualTo('password', message='Must match %(other_label)s')])


class BeerStyleTypeForm(Form):
    name = TextField('Style Type Name', [validators.Length(min=3, max=35)])
    description = TextAreaField('Description')


class BeerStyleForm(Form):
    name = TextField('Style Name', [validators.Length(min=3, max=35)])
    description = TextAreaField('Description')
    style_type = QuerySelectField('Type', query_factory=lambda: db.session.query(models.BeerStyleType),
                                  get_pk=lambda a: a.id, get_label=lambda a: a.name)
    link_ratebeer = TextField('Link (www.ratebeer.com)', [validators.URL, validators.Length(max=255)])
    link_beeradvocate = TextField('Link (www.beeradvocate.com)', [validators.URL, validators.Length(max=255)])


class BeerForm(Form):
    hex = TextField('Hex Code', [validators.Length(min=1, max=5)])
    name = TextField('Name', [validators.Length(min=3, max=35)])
    style = QuerySelectField('Style', query_factory=lambda: db.session.query(models.BeerStyle),
                             get_pk=lambda a: a.id, get_label=lambda a: a.name)
    description = TextAreaField('Description')
    recipe = TextAreaField('Recipe')
    gallons = TextField('Volume (Gallons)', [validators.Length(max=10)])
    date_brewed = TextField('Date Brewed', [validators.Length(max=10)])
    date_bottled = TextField('Date Bottled', [validators.Length(max=10)])
    gravity_og = TextField('Gravity (Original)', [validators.Length(max=10)])
    gravity_fg = TextField('Gravity (Final)', [validators.Length(max=10)])

