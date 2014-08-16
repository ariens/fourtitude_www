from fourtitude import lm, db
from config import ACTIVATION_CODE_VALID_FOR_SECONDS
import string
import random
from datetime import timedelta, datetime


class BeerStyleType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    description = db.Column(db.Text)

    def __str__(self):
        return self.name

    @staticmethod
    def get_label():
        return "Style Type"

    @staticmethod
    def get_template():
        return "beer/manage_style_type.html"


class BeerStyle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    description = db.Column(db.Text)
    link_beeradvocate = db.Column(db.String(255))
    link_ratebeer = db.Column(db.String(255))
    style_type_id = db.Column(db.Integer, db.ForeignKey('beer_style_type.id'))
    style_type = db.relationship('BeerStyleType', backref=db.backref('beer_style', lazy='dynamic'))

    def __str__(self):
        return self.name

    @staticmethod
    def get_label():
        return "Style"

    @staticmethod
    def get_template():
        return "beer/manage_style.html"


class Beer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    description = db.Column(db.Text)
    style_id = db.Column(db.Integer, db.ForeignKey('beer_style.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    first_name = db.Column(db.String(35))
    last_name = db.Column(db.String(35))
    primary_email_id = db.Column(db.Integer)
    password_digest = db.Column(db.String(60))
    self_deleted = db.Column(db.Boolean, default=False)
    admin_disabled = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def add_to_users_group(self):
        users_group = UserGroup.query.filter_by(name='users').first()
        users_membership = UserGroupMembership()
        users_membership.user_id = self.id
        users_membership.user_group_id = users_group.id
        db.session.add(users_membership)
        db.session.commit()

    @staticmethod
    def is_authenticated():
        return True

    #TODO: is_active needs a re-write, doesn't make sense now that the user_email_addresses table exists
    def is_active(self):
        if EmailActivation.query.filter_by(user_id=self.id, activated=True).first() is None:
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


class UserEmailAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    email_address = db.Column(db.String(255), unique=True)
    confirmed = db.Column(db.Boolean, default=False)


class UserGroupException(Exception):
    pass


class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))

    def has_member(self, user):
        membership = UserGroupMembership.query.filter_by(user_group_id=self.id, user_id=user.id).first()
        if membership is None:
            return False
        else:
            return True


class UserGroupMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user_group_id = db.Column(db.Integer, db.ForeignKey(UserGroup.id))


class EmailActivationException(Exception):
    pass


class EmailActivation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    email_address_id = db.Column(db.Integer)
    activation_code = db.Column(db.String(25), unique=True)
    activated = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime)
    date_expires = db.Column(db.DateTime)

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
        db.session.add(activation)
        db.session.commit()
        return activation


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
