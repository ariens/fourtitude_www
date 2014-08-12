from flask.ext.mail import Message
from app import mail
from .models import User, UserEmailAddress
from flask import render_template


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_user_email_activation(email_activation):
    user = User.query.filter_by(id=email_activation.user_id).first()
    email_address = UserEmailAddress.query.filter_by(id=email_activation.email_address_id).first()
    send_email("[www.fourtitude.ca] Activate Your Account",
               "dave@ariens.ca",
               [email_address.email_address],
               render_template("auth/emails/email_activate_account.txt", user=user, activation=email_activation),
               render_template("auth/emails/email_activate_account.html", user=user, activation=email_activation))

def send_reset_password_activation(email_activation):
    user = User.query.filter_by(id=email_activation.user_id).first()
    email_address = UserEmailAddress.query.filter_by(id=email_activation.email_address_id).first()
    send_email("[www.fourtitude.ca] Reset Your Password",
               "dave@ariens.ca",
               [email_address.email_address],
               render_template("auth/emails/email_password_reset.txt", user=user, activation=email_activation),
               render_template("auth/emails/email_password_reset.html", user=user, activation=email_activation))
