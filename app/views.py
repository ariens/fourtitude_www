import os

from app import app, lm, db
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import current_user, UserMixin
from .models import User, EmailActivation
from . import forms 
from . import models
from . import emails


@app.route('/')
def index():
    user = {'nickname': "dave", 'full_name': "Dave Ariens"}
    return render_template(
        "index.html",
        title="Home",
        user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    #registration = None;
    form = forms.RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                role=models.ROLE_USER)
            db.session.add(new_user)
            db.session.commit()
            new_user_email_activation = EmailActivation(new_user.id)
            db.session.add(new_user_email_activation)
            db.session.commit()
            emails.send_user_email_activation(new_user_email_activation)
            db.session.commit()
            flash("Please check your e-mail for activation instructions")
        else:
            flash("That e-mail address has already been registered on this site")
    return render_template(
        'register.html',
        title='Register',
        form=form)


@app.route('/email_activation', methods=['GET', 'POST'])
def email_activation():
    flash("the activation code is: " + request.args['confirmation_code'])
    user=User.query.filter_by(email_activation=request.args['confirmation_code'])

    return render_template(
        'email_activation.html',
        title='Activate Your Account')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    return render_template(
        'login.html',
        title='Login',
        form=form)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))