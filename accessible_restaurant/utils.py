from django.conf import settings
# from django.forms.models import model_to_dict
from .models import Restaurant

import requests
import json

def get_restaurant_data(business_id):
    if not business_id:
        return None
    token = settings.YELP_TOKEN
    headers = {'Authorization': 'bearer %s' % token}
    url = settings.YELP_REST_ENDPOINT + business_id
    response = requests.request(url, headers=headers)
    return json.load(response.text)

def get_restaurant_reviews(business_id):
    if not business_id:
        return None
    token = settings.YELP_TOKEN
    headers = {'Authorization': 'bearer %s' % token}
    url = settings.YELP_REST_ENDPOINT + business_id + '/reviews'
    response = requests.request(url, headers=headers)
    return json.load(response.text)

def get_restaurant(business_id):
    if not business_id:
        return None
    response = {
        "restaurant_data": get_restaurant_data(business_id),
        "restaurant_reviews": get_restaurant_reviews(business_id)
    }
    return response

def get_restaurant_list(page, size):
    offset = int(page) * int(size)
    restaurants = Restaurant.objects.all()[offset : offset + size]
    response = []
    for restaurant in restaurants:
        response.append(restaurant.__dict__)

    return response