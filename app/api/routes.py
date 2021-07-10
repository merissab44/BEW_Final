from app.models import Restaurant, Review, User
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.api.forms import DataForm, RestaurantForm, ReviewForm
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

# add restaurants to database
for restaurant in category_data['businesses']:
    # print(restaurant['name'], restaurant['location']['display_address'], restaurant['id'])

    existing_restaurant = Restaurant.query.get(restaurant['id'])
    if not existing_restaurant:
        r = Restaurant(id=restaurant['id'], name=restaurant['name'], address=restaurant['location']['address1'], price=restaurant['price'])
        db.session.add(r)
        db.session.commit()
        print('I have added the restaurants to the database')

#check the database to see if the restuarant was added 

@api.route('/')
def displayWelcomePage():
    return render_template('base.html')

@login_required
@api.route('/feed')
def display_categories():
    business_array = []
    for biz in category_data['businesses']:
        business_array.append(biz)
    # print(business_array[0]['name'])
    return render_template('feed.html', restaurants=business_array)
    
@api.route('/restaurant_detail/<review_id>', methods=['GET', 'POST'])
def restaurant_detail(review_id):
    reviews = Review.query.get(review_id)
    restaurant = Restaurant.query.get(reviews.restaurant_id)
    # user = User.query.get(user_id)
    form = RestaurantForm(obj=restaurant)
    return render_template('restaurant_detail.html',restaurant=restaurant, form=form, reviews=reviews)

@login_required
@api.route('/review/<restaurant_id>/<user_id>', methods=['GET','POST'])
def leave_review(restaurant_id, user_id):
    # restaurant = Restaurant.query.get(restaurant_id)
    # user = User.query.get(user_id)
    # print(user)
    form = ReviewForm()
    if form.validate_on_submit():
        print("form is validated")
        new_review = Review(
            user_id = user_id,
            restaurant_id = restaurant_id,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(new_review)
        db.session.commit()
        flash('has added a review!')
        return redirect(url_for('api.restaurant_detail', review_id = new_review.id))
    return render_template('review.html', form=form, restaurant=restaurant)


@api.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)

@api.route('/listings')
def listing():
    try:
        return render_template('listing.html')
    except (ValueError, TypeError):
        return render_template('500.html'), 500
