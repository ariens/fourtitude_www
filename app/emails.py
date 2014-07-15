from flask.ext.mail import Message
from app import mail
from flask import render_template
from config import ADMINS
from threading import Thread

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_user_activation(new_user):
    send_email("[www.fourtitude.ca] Activate Your Account",
        "dave@ariens.ca",
        [new_user.email],
        render_template("activate_email.txt", user = new_user),
        render_template("activate_email.html", user = new_user))
