from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Review, Restaurant
from app.auth.forms import SignUpForm, LoginForm
from app import bcrypt

# Import app and db from events_app package so that we can run app
from app import app, db

main = Blueprint('main', __name__)