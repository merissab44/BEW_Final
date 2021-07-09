# Create your tests here.
import os
import unittest

from unittest import TestCase

from datetime import date

from app import app, db, bcrypt
from app.models import Review, Restaurant, User

"""
Run these tests with the command:
python -m unittest books_app.auth.tests
"""

#SETUP

def create_user():
    password_hash = bcrypt.generate_password_hash("password").decode("utf-8")
    user = User(username="merissa", password=password_hash)
    db.session.add(user)
    db.session.commit()

#TESTS

class AuthTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def signup_existing_user(self):
        """ If user is trying to sign up but they already 
        exist in database, it should return an error message """
        create_user()
        post_data = {"username": "audrey", "password": "tiger"}
        response = self.app.post("/signup", data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn(
            "That username is taken. Please choose a different one.", response_text
        )

    def login_incorrect_password(self):
        """when user logs in with incorrect password, it should return an error message """
        create_user()
        post_data = {"username": "me1", "password": "password_hash"}
        response = self.app.post("/login", data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn("Password is incorrect. Please try again.", response_text)
    
    def login_incorrect_username(self):
        """when user logs in with incorrect username, it should return an error message """
        create_user()
        post_data = {"username": "merissa", "password": "tiger"}
        response = self.app.post("/login", data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn("No user with that username. Please try again.", response_text)

   