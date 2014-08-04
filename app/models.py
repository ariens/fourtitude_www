import app
from config import ACTIVATION_CODE_VALID_FOR_SECONDS
import string
import random
from datetime import timedelta
from datetime import datetime

ROLE_USER = 0
ROLE_ADMIN = 1


class User(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    username = app.db.Column(app.db.String(64), unique=True)
    email = app.db.Column(app.db.String(120), unique=True)
    role = app.db.Column(app.db.SmallInteger, default=ROLE_USER)

    @staticmethod
    def is_authenticated():
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


class EmailActivation(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    user_id = app.db.Column(app.db.Integer, app.db.ForeignKey(User.id))
    activation_code = app.db.Column(app.db.String(25), unique=True)
    activated = app.db.Column(app.db.Boolean, default=False)
    date_created = app.db.Column(app.db.DateTime)
    date_expires = app.db.Column(app.db.DateTime)

    def __init__(self, user_id, activated=False, date_created=datetime.utcnow()):
        self.user_id = user_id
        self.activation_code = self.gen_unique_user_activation_code()
        self.activated = activated
        self.date_created = date_created
        self.date_expires = self.date_created + timedelta(0, ACTIVATION_CODE_VALID_FOR_SECONDS)

    @staticmethod
    def gen_random_activation_code(size=25, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def gen_unique_user_activation_code():
        activation_code = EmailActivation.gen_random_activation_code()
        while EmailActivation.query.filter_by(activation_code=activation_code).first() is not None:
            activation_code = EmailActivation.gen_random_activation_code()
        return activation_code

@app.lm.user_loader
def load_user(id):
    return User.query.get(int(id))
