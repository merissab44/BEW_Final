from app.models import Restaurant
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.api.forms import DataForm, RestaurantForm
import os
import json
import requests
from dotenv import load_dotenv
from app import bcrypt

from app import app,db

api = Blueprint('api', __name__)

load_dotenv()
# Define API KEY, ENDPOINTS, AND HEADERS HERE
API_KEY = os.getenv('API_KEY')
API_URL = 'https://api.yelp.com/v3'
BUSINESS_ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}
# Define our parameters
PARAMETERS = {
    'categories': 'food',
    'limit': 20,
    'radius': 10000,
    'price': 1,
    'is_close': False,
    'location': 'Oakland'
}
# Make a request to the API
response = requests.get(url=BUSINESS_ENDPOINT,
                        params=PARAMETERS, headers=HEADERS)


# Converts the json string to a dictionary
category_data = response.json()

@api.route('/')
def displayWelcomePage():
    return render_template('base.html')

@api.route('/data', methods=['GET', 'POST'])
def dataform():
    form = DataForm()
    if form.validate_on_submit():
        #here is where I want to define the location parameter
        PARAMETERS['location'] = form.location.data
        return redirect(url_for('api.feed', form=form))
    return render_template('data.html')

@api.route('/feed')
def display_categories():
    business_array = []
    for biz in category_data['businesses']:
        business_array.append(biz)
    # print(business_array[0]['name'])
    return render_template('feed.html', context=business_array)
    
@api.route('/restaurant_detail/<restaurant_id>', methods=['GET', 'POST'])
def detail(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    return render_template('restaurant_detail.html',restaurant=restaurant)

@login_required
@api.route('/add_restaurant', methods=['GET','POST'])
def create_restaurant():
    form = RestaurantForm()
    if form.validate_on_submit():
        new_restaurant = Restaurant(
            name=form.name.data,
            price_range= form.price_range.data,
            location=form.location.data
        )
        db.session.add(new_restaurant)
        db.session.commit()
        flash('Restaurant has been added!')
        return redirect(url_for('api.feed', restaurant_id = new_restaurant.id))
    return render_template('add_restaurant.html',form=form)

@api.route('/listings')
def listing():
    try:
        return render_template('listing.html')
    except (ValueError, TypeError):
        return render_template('500.html'), 500
