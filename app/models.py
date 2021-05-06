# Create your models here.
from app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class User():
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    reviews = db.relationship('Review', back_populates='user')
    restaurants = db.relationship('Restaurant', back_populates='user')


class Review():
    id = db.Column(db.Integer, primary_key=True)
    #user that wrote the review
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    user = db.relationship('User', back_populates='reviews')
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(480))


class Restaurant():
    id = db.Column(db.Integer, primary_key=True)
    #user that created the restaurant listing
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    user =  user = db.relationship('User', back_populates='restaurants')
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False) 