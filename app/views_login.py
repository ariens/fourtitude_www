from flask import render_template, flash, redirect, session, url_for, request, g
import flask_login
from flask_login import logout_user
from app import app, lm, crypto
from .models import User, UserEmailAddress
from . import forms


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


class LoginException(Exception):
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    problem = None
    form = forms.LoginForm()
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    try:
        if form.validate_on_submit():
            session['remember_me'] = form.remember_me.data
            email = UserEmailAddress.query.filter_by(email_address=form.email.data).first()
            if email is None:
                problem = "email"
                raise LoginException("That account does not exist")
            user = User.query.filter_by(id=email.user_id).first()
            if user is None:
                problem = "email"
                raise LoginException("Unknown account associated to that e-mail address")
            if not crypto.is_password(form.password.data, user.password_digest):
                problem = "password"
                raise LoginException("Invalid password")
            if email.confirmed is False:
                problem = "inactive"
                raise LoginException("Your account hasn't been activated yet")
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            flask_login.login_user(user, remember=remember_me)
            return redirect(request.args.get('next') or url_for('index'))
    except LoginException as error:
        flash(error)
    return render_template(
        'auth/page_login.html',
        problem=problem,
        title='Login',
        form=form)