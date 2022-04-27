from flask_login import UserMixin
from . import db

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(16))
    num_shares = db.Column(db.Float)
    b_price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    stocks = db.relationship('Stock')
