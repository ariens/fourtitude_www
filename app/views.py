from flask import render_template, g
from flask_login import current_user
from app import lm, app, models


@lm.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user



@app.route('/')
def index():
    user = g.user
    return render_template(
        "home/page.html",
        title="Home",
        user=user)


@app.errorhandler(403)
def forbidden_403(exception):
    user = g.user
    return render_template(
        "http_codes/403.html",
        title="403 - Forbidden",
        user=user)
