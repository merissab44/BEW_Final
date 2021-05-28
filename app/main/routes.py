from app.models import Restaurant
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.api.forms import DataForm
import os
# from flask_pymongo import PyMongo
import json
import requests
from dotenv import load_dotenv
from app import bcrypt

from app import app,db

api = Blueprint('api', __name__)    
# Import app and db from events_app package so that we can run app
from app import app, db

main = Blueprint('main', __name__)

@main.route('/data', methods=['GET', 'POST'])
def location():
    form = DataForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('api.feed'))
    return render_template('data.html', form=form)