import app
import string
import random

ROLE_USER = 0
ROLE_ADMIN = 1


class EmailActivation(app.db.model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    user_id = app.db.Column.Integer, app.db.ForeignKey(User.id)
    activation_code = app.db.Column(app.db.String(25), unique=True)
    verified = app.db.Column(app.db.Boolean, default=False)
    date_created =


class User(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    username = app.db.Column(app.db.String(64), unique=True)
    email = app.db.Column(app.db.String(120), unique=True)
    role = app.db.Column(app.db.SmallInteger, default=ROLE_USER)
    email_activation_code =     app.db.Column(app.db.String(25), unique=True)
    email_verified = app.db.Column(app.db.Boolean, default=False)

    @staticmethod
    def generate_email_activation_code(size=25, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def is_authenticated():
        return True

    def is_active(self):
        return self.email_verified

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


@app.lm.user_loader
def load_user(id):
    return User.query.get(int(id))
