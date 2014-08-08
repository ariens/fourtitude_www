from flask import render_template, g
from flask_login import current_user
from app import app


@app.route('/')
def index():
    user = g.user
    return render_template(
        "index.html",
        title="Home",
        user=user)


@app.before_request
def before_request():
    g.user = current_user