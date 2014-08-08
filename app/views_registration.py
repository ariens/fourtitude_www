from flask import render_template, flash, redirect, url_for, request
from app import app, db, crypto
from .models import User, UserEmailAddress, EmailActivation, EmailActivationException
from . import forms
from . import emails


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
                problem = "invalid_email"
                raise SendActivationException("Unknown e-mail address")
            user = User.query.filter_by(id=email.user_id).first()
            if user is None:
                problem = "unknown_user"
                raise SendActivationException("Unknown account associated to that e-mail address")
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
