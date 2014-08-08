import os

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
mail = Mail(app)

from app import models
from app import views, views_beer, views_login, views_registration, views_password_reset

