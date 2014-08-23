from fourtitude import db
from datetime import datetime
from flask import g


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('article', lazy='dynamic'))
    title = db.Column(db.String(50))
    body = db.Column(db.Text())

    def __repr__(self):
        return '<Article %r>' % self.title

    @staticmethod
    def get_auto_manage_label():
        return "Article"

    @staticmethod
    def manage_template():
        return "article/manage_article.html"

    @staticmethod
    def delete_template():
        return "article/delete_article.html"

    def foreign_key_protected(self):
        return True

    def form_populate_helper(self):
        if self.date_posted is None or self.date_posted == '':
            self.date_posted = datetime.utcnow()
        if self.user_id is None:
            self.user_id = g.user.id
            self.user = g.user
