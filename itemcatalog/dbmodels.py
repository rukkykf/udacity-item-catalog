from datetime import datetime

from itemcatalog.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), nullable=False)


class Password(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey(
        "user.id"), nullable=False, primary_key=True)
    pw_hash = db.Column(db.String(256), nullable=False, unique=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    categoryid = db.Column(db.Integer, db.ForeignKey("category.id"))
    pubdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.relationship('Category', backref=db.backref('items', lazy=True))

    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', backref=db.backref('items', lazy=True))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    pubdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    itemid = db.Column(db.Integer, db.ForeignKey("item.id"))


class Like(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey(
        "user.id"), nullable=False, primary_key=True)
    itemid = db.Column(db.Integer, db.ForeignKey(
        "item.id"), nullable=False, primary_key=True)
