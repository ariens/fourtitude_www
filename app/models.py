import app
from config import ACTIVATION_CODE_VALID_FOR_SECONDS
import string
import random
from datetime import timedelta
from datetime import datetime

class User(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    username = app.db.Column(app.db.String(64), unique=True)
    first_name = app.db.Column(app.db.String(35))
    last_name = app.db.Column(app.db.String(35))
    primary_email_id = app.db.Column(app.db.Integer)
    password_digest = app.db.Column(app.db.String(60))
    self_deleted = app.db.Column(app.db.Boolean, default=False)
    admin_disabled = app.db.Column(app.db.Boolean, default=False)

    @staticmethod
    def is_authenticated():
        return True

    def is_active(self):
        if EmailActivation.query.filter_by(user_id=self.id, activated=False).first() is not None:
            return False

        return True

    def email_activated(self):
        if EmailActivation.query.filter_by(user_id=self.id).first() is None:
                return True
        else:
                return False

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class UserEmailAddress(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    user_id = app.db.Column(app.db.Integer, app.db.ForeignKey(User.id))
    email_address = app.db.Column(app.db.String(255), unique=True)
    confirmed = app.db.Column(app.db.Boolean, default=False)


class EmailActivationException(Exception):
    pass


class EmailActivation(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    user_id = app.db.Column(app.db.Integer, app.db.ForeignKey(User.id))
    email_address_id = app.db.Column(app.db.Integer)
    activation_code = app.db.Column(app.db.String(25), unique=True)
    activated = app.db.Column(app.db.Boolean, default=False)
    date_created = app.db.Column(app.db.DateTime)
    date_expires = app.db.Column(app.db.DateTime)

    def __init__(self, user_id, email_address_id, activated=False, date_created=datetime.utcnow()):
        self.user_id = user_id
        self.email_address_id = email_address_id
        self.activation_code = self.gen_unique_activation_code()
        self.activated = activated
        self.date_created = date_created
        self.date_expires = self.date_created + timedelta(0, ACTIVATION_CODE_VALID_FOR_SECONDS)

    @staticmethod
    def gen_random_activation_code(size=25, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def gen_unique_activation_code():
        activation_code = EmailActivation.gen_random_activation_code()
        while EmailActivation.query.filter_by(activation_code=activation_code).first() is not None:
            activation_code = EmailActivation.gen_random_activation_code()
        return activation_code

    def expired(self):
        if datetime.utcnow() > self.date_expires:
            return True
        else:
            return False

    @staticmethod
    def activate(activation_code):
        activation = EmailActivation.query.filter_by(activation_code=activation_code).first()
        if activation is None:
            raise EmailActivationException("Cannot find that activation code")
        if activation.activated is True:
            raise EmailActivationException("That code has already been activated")
        if activation.expired is True:
            raise EmailActivationException("That activation code expired on ", activation.date_expires)
        activation.activated = True
        app.db.session.add(activation)
        app.db.session.commit()
        return activation


@app.lm.user_loader
def load_user(id):
    return User.query.get(int(id))
