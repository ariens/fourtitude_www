import os


from flask import render_template, flash, redirect, session, url_for, request, g
import flask_login
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm, db, crypto
from .models import User, EmailActivation, EmailActivationException
from . import forms 
from . import models
from . import emails


@app.route('/')
@login_required
def index():
    user = g.user
    return render_template(
        "index.html",
        title="Home",
        user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            new_user = User(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                role=models.ROLE_USER,
                password_digest=crypto.get_digest(form.password.data))
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Invalid e-mail/password, please try again')
        elif crypto.is_password(form.password.data, user.password_digest):
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            flask_login.login_user(user, remember=remember_me)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Invalid e-mail/password, please try again')
    return render_template(
        'login.html',
        title='Login',
        form=form)


@app.route('/email_activation', methods=['GET', 'POST'])
def email_activation():
    """
    This is the route that a user accesses when activating their e-mail address
    :return:
    """
    try:
        activation = EmailActivation.activate_via_activation_code(request.args['confirmation_code'])
        new_user = User.query.filter_by(id=activation.user_id).first()
        flash("E-mail address " + new_user.email + " has been successfully activated, you may now login")
        return redirect(url_for('login'))
    except EmailActivationException as err:
        flash("Error activating that e-mail address: {0}".format(err))
    return render_template(
        'email_activation.html',
        title='Activate Your Account')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))