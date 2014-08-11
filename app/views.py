from flask import render_template, g
from flask_login import current_user
from app import app


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