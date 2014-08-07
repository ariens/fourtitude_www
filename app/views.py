from flask import render_template, flash, redirect, session, url_for, request, g
import flask_login
from flask_login import logout_user, current_user, login_required
from app import app, lm, db, crypto
from .models import User, UserEmailAddress, EmailActivation, EmailActivationException
from . import forms
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
        #todo: try
        email_address = UserEmailAddress.query.filter_by(email_address=form.email.data).first()
        username = User.query.filter_by(username=form.username.data).first()
        if username is not None:
            flash("The username \"" + form.username.data + "\" is already taken")
        elif email_address is not None:
            flash("That e-mail address has already been registered on this site")
        else:
            new_user = User(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password_digest=crypto.get_digest(form.password.data))
            db.session.add(new_user)
            db.session.commit()
            new_user.add_to_users_group()

            new_email_address = UserEmailAddress(
                user_id=new_user.id,
                email_address=form.email.data)
            db.session.add(new_email_address)
            db.session.commit()

            activation = EmailActivation(
                user_id=new_user.id,
                email_address_id=new_email_address.id)
            db.session.add(activation)
            db.session.commit()

            new_user.primary_email_id = new_email_address.id
            db.session.add(new_user)
            db.session.commit()

            emails.send_user_email_activation(activation)
            flash("Please check your e-mail for activation instructions")
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


class LoginException(Exception):
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    problem = None
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    try:
        form = forms.LoginForm()
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
        'login.html',
        problem=problem,
        title='Login',
        form=form)


@app.route('/email_activation', methods=['GET', 'POST'])
def email_activation():
    """
    This is the route that a user accesses when activating their e-mail address
    :return:
    """
    try:
        activation = EmailActivation.activate(request.args['confirmation_code'])
        email_address = UserEmailAddress.query.filter_by(id=activation.email_address_id).first()
        email_address.confirmed = True
        db.session.add(email_address)
        db.session.commit()
        flash("E-mail address " + email_address.email_address + " activated, you may now login")
        return redirect(url_for('login'))
    except EmailActivationException as err:
        flash("Error activating that e-mail address: {0}".format(err))
    return render_template(
        'email_activation.html',
        title='Activate Your Account')


class SendActivationException(Exception):
    pass


@app.route('/send_activation', methods=['GET', 'POST'])
def send_activation():
    """
    This is the route that a user accesses when re-sending their activation e-mail
    :return: rendered template
    """
    problem = None
    form = forms.EmailOnly()
    if form.validate_on_submit():
        try:
            email = UserEmailAddress.query.filter_by(email_address=form.email.data).first()
            if email is None:
                problem="invalid_email"
                raise SendActivationException("Unknown e-mail address")
            user = User.query.filter_by(id=email.user_id).first()
            if user is None:
                problem = "unknown_user"
                raise LoginException("Unknown account associated to that e-mail address")
            new_activation = EmailActivation(user_id=user.id, email_address_id=email.id)
            db.session.add(new_activation)
            emails.send_user_email_activation(new_activation)
            db.session.add(new_activation)
            db.session.commit()
            flash("Check your e-mail, we sent a new activation code to " + email.email_address)
            #TODO add a generic activation template here.
        except SendActivationException as error:
            flash(error)
    return render_template(
        'send_activation.html',
        problem=problem,
        title='Send New Activation',
        form=form)


class RequestPasswordResetException(Exception):
    pass


@app.route('/request_password_reset', methods=['GET', 'POST'])
def request_password_reset():
    """
    This is the route that a user accesses when they need to reset their password
    :return: rendered template
    """
    problem = None
    form = forms.EmailOnly()
    if form.validate_on_submit():
        try:
            email = UserEmailAddress.query.filter_by(email_address=form.email.data).first()
            if email is None:
                problem = "invalid_email"
                raise RequestPasswordResetException("Unknown e-mail address")
            user = User.query.filter_by(id=email.user_id).first()
            if user is None:
                problem = "unknown_user"
                raise RequestPasswordResetException("Unknown account associated to that e-mail address")
            new_activation = EmailActivation(user_id=user.id, email_address_id=email.id)
            db.session.add(new_activation)
            db.session.commit()
            emails.send_reset_password_activation(new_activation)
            flash("Check your e-mail, we sent the password reset request to " + email.email_address)
        except RequestPasswordResetException as error:
            flash(error)
    return render_template(
        'request_password_reset.html',
        problem=problem,
        title='Request Password Reset',
        form=form)


class PasswordResetException(Exception):
    pass


@app.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    """
    This is the route that a user accesses when they are resetting their password
    :return: rendered template
    """
    problem = None
    try:
        form = forms.PasswordReset(activation_code=request.args['confirmation_code'])
        if form.validate_on_submit():
            activation = EmailActivation.query.filter_by(activation_code=request.args['confirmation_code']).first()
            if activation is None:
                problem = "invalid_code"
                raise PasswordResetException("Invalid activation code")
            if activation.activated is True:
                problem = "already_activated"
                raise PasswordResetException("That activation code has already been activated")
            if activation.expired() is True:
                problem = "expired"
                raise PasswordResetException("That activation code is expired")
            user = User.query.filter_by(id=activation.user_id).first()
            if user is None:
                problem = "unknown_user"
                raise PasswordResetException("Unknown account associated to that e-mail address")
            user.password_digest = crypto.get_digest(form.password.data)
            db.session.add(user)
            EmailActivation.activate(activation.activation_code)
            db.session.commit()
            flash("Your password has been reset, please remember to login with your new password")
            return redirect(url_for('login'))
    except PasswordResetException as error:
        flash(error)
    except EmailActivationException as error:
        flash(error)
    return render_template(
        'password_reset.html',
        problem=problem,
        title='Request Password Reset',
        form=form)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
