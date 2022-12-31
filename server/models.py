from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime
from sqlalchemy.inspection import inspect

db = SQLAlchemy()


def get_uuid():
    return uuid4().hex


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class User(db.Model, Serializer):
    __tablename__ = "user"

    id = db.Column(db.String(32), primary_key=True,
                   unique=True, default=get_uuid)
    username = db.Column(db.String(80), unique=True,  nullable=False)
    hash = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def serialize(self):
        d = Serializer.serialize(self)
        del d['hash']
        return d


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey(
        'user.id'))
    status = db.Column(db.String(10))
    items = db.relationship('Order_Item', backref='order', lazy=True)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Order_Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    image = db.Column(db.String(100))
    title = db.Column(db.String(50))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    price = db.Column(db.Float)

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey(
        'user.id'))
    title = db.Column(db.String(50), unique=True)
    price = db.Column(db.Float)
    category = db.Column(db.String(50))
    description = db.Column(db.String(120))
    image = db.Column(db.String(100))
    orders = db.relationship('Order_Item', backref='product', lazy=True)

    def serialize(self):
        d = Serializer.serialize(self)
        del d['orders']
        return d
