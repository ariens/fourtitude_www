from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
mail = Mail(app)

from . import views
from . import beer_views
from . import user_views
from . import article_views

from .momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs