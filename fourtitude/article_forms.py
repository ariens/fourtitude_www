from flask.ext.wtf import Form
from wtforms import TextField, validators, TextAreaField


class ArticleForm(Form):
    title = TextField('Name', [validators.Length(min=3, max=35)])
    body = TextAreaField('Body')
