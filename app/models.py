# Create your models here.
from app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    reviews = db.relationship('Review', back_populates='user')
    # restaurants = db.relationship('Restaurant', back_populates='user')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #user that wrote the review
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    user = db.relationship('User', back_populates='reviews')
    restaurant = db.relationship('Restaurant', back_populates='reviews')
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(480))


class Restaurant(db.Model):
    id = db.Column(db.String, primary_key=True)
    reviews = db.relationship('Review', back_populates='restaurant')
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50), nullable=False) 
