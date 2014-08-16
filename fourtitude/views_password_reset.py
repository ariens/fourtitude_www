from flask import render_template, flash, redirect, url_for, request
from fourtitude import app, db, crypto
from .models import User, UserEmailAddress, EmailActivation, EmailActivationException
from . import forms, emails


class PasswordResetException(Exception):
    pass


@app.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    """
    This is the route that a user accesses when they are resetting their password
    :return: rendered template
    """
    problem = None
    form = forms.PasswordReset(activation_code=request.args['confirmation_code'])
    try:
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
        'auth/page_password_reset.html',
        problem=problem,
        title='Request Password Reset',
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
        'auth/page_request_password_reset.html',
        problem=problem,
        title='Request Password Reset',
        form=form)