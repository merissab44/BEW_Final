from flask import Blueprint, request, render_template, redirect, url_for, flash
import os
from flask_pymongo import PyMongo
import json
from dotenv import load_dotenv

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
# print(category_data)


# print(business_name)
# print(rating)


@api.route('/')
def displayWelcomePage():
    return render_template('index.html')


@api.route('/home')
def display_categories():
    business_array = []
    for biz in category_data['businesses']:
        business_array.apiend(biz)
        # print(biz)

    # context = {
    #     'name': business_array['name'],
    #     'photo': business_array['image_url'],
    #     'price': business_array['price'],
    #     'address': business_array['location']
    # }
    print(business_array[0]['name'])
    return render_template('home.html', context=business_array)


@api.route('/about')
def meetUs():
    return render_template('about.html')


@api.route('/feed')
def feedPage():
    return render_template('feed.html')


@api.route('/post')
def postPage():
    return render_template('post.html')


@api.route('/listings')
def listing():
    try:
        return render_template('listing.html')
    except (ValueError, TypeError):
        return render_template('500.html'), 500
