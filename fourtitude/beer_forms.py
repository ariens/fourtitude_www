from flask.ext.wtf import Form
import fourtitude
from wtforms import validators, TextAreaField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from fourtitude import db


class BeerForm(Form):
    hex = StringField('Hex Code', [validators.Length(min=1, max=5)])
    name = StringField('Name', [validators.Length(min=3, max=35)])
    style = QuerySelectField('Style',
                             query_factory=lambda: db.session.query(fourtitude.beer_models.BeerStyle),
                             get_pk=lambda a: a.id, get_label=lambda a: a.name)
    description = TextAreaField('Description')
    recipe = TextAreaField('Recipe')
    gallons = StringField('Volume (Gallons)', [validators.Length(max=10)])
    date_brewed = StringField('Date Brewed', [validators.Length(max=10)])
    date_bottled = StringField('Date Bottled', [validators.Length(max=10)])
    gravity_og = StringField('Gravity (Original)', [validators.Length(max=10)])
    gravity_fg = StringField('Gravity (Final)', [validators.Length(max=10)])


class BeerStyleForm(Form):
    name = StringField('Style Name', [validators.Length(min=3, max=35)])
    description = TextAreaField('Description')
    style_type = QuerySelectField('Type',
                                  query_factory=lambda: db.session.query(fourtitude.beer_models.BeerStyleType),
                                  get_pk=lambda a: a.id, get_label=lambda a: a.name)
    link_ratebeer = StringField('Link (www.ratebeer.com)', [validators.URL, validators.Length(max=255)])
    link_beeradvocate = StringField('Link (www.beeradvocate.com)', [validators.URL, validators.Length(max=255)])


class BeerStyleTypeForm(Form):
    name = StringField('Style Type Name', [validators.Length(min=3, max=35)])
    description = TextAreaField('Description')