from fourtitude import db
from datetime import datetime
from fourtitude.managed_object import ManagedObject


class BeerStyleType(db.Model, ManagedObject):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    description = db.Column(db.Text)

    def __str__(self):
        return self.name

    @staticmethod
    def get_auto_manage_label():
        return "Beer Style Type"

    @staticmethod
    def manage_template():
        return "beer/manage_beer_style_type.html"

    @staticmethod
    def delete_template():
        return "beer/delete_beer_style_type.html"

    def foreign_key_protected(self):
        return BeerStyle.query.filter_by(style_type_id=self.id).first() is None


class BeerStyle(db.Model, ManagedObject):
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
    def get_auto_manage_label():
        return "Beer Style"

    @staticmethod
    def manage_template():
        return "beer/manage_beer_style.html"

    @staticmethod
    def delete_template():
        return "beer/delete_beer_style.html"

    def foreign_key_protected(self):
        return Beer.query.filter_by(style_id=self.id).first() is None


class Beer(db.Model, ManagedObject):
    id = db.Column(db.Integer, primary_key=True)
    hex = db.Column(db.String(5))
    name = db.Column(db.String(35))
    description = db.Column(db.Text)
    recipe = db.Column(db.Text)
    gallons = db.Column(db.Integer)
    date_brewed = db.Column(db.Date)
    date_bottled = db.Column(db.Date)
    gravity_og = db.Column(db.Integer)
    gravity_fg = db.Column(db.Integer)
    style_id = db.Column(db.Integer, db.ForeignKey('beer_style.id'))
    style = db.relationship('BeerStyle', backref=db.backref('beer', lazy='dynamic'))

    def __str__(self):
        return self.name

    @staticmethod
    def get_auto_manage_label():
        return "Beer"

    @staticmethod
    def manage_template():
        return "beer/manage_beer.html"

    @staticmethod
    def delete_template():
        return "beer/delete_beer.html"

    def form_populate_helper(self):
        if self.date_brewed is not None and self.date_brewed != "":
            self.date_brewed = datetime.strptime(str(self.date_brewed), '%Y-%m-%d').date()
        else:
            self.date_brewed = datetime.today().date()
        if self.date_bottled is not None and self.date_bottled != "":
            self.date_bottled = datetime.strptime(str(self.date_bottled), '%Y-%m-%d').date()
        else:
            self.date_bottled = datetime.today().date()

    def foreign_key_protected(self):
        return True

    def get_abv(self):
        if self.gravity_fg is not None and self.gravity_og is not None:
            if self.gravity_fg != "" and self.gravity_og != "":
                return "- {0:4.1f}% ABV".format((self.gravity_og - self.gravity_fg) * 131)
