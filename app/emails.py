from flask.ext.mail import Message
from app import mail
from .models import User
from flask import render_template


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_user_email_activation(email_activation):
    user = User.query.filter_by(id=email_activation.user_id).first()
    print("the user is: ", user)
    print("user email is: ", user.email)
    send_email("[www.fourtitude.ca] Activate Your Account",
               "dave@ariens.ca",
               [user.email],
               render_template("activate_email.txt", user=user, activation=email_activation),
               render_template("activate_email.html", user=user, activation=email_activation))
