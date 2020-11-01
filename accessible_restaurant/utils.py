from django.conf import settings
from .models import Restaurant
import requests
import json
import math

from django.contrib.gis.geoip2 import GeoIP2


def get_restaurant_data(business_id):
    if not business_id:
        return None
    token = settings.YELP_TOKEN
    headers = {"Authorization": "bearer %s" % token}
    url = settings.YELP_REST_ENDPOINT + business_id
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_restaurant_reviews(business_id):
    if not business_id:
        return None
    token = settings.YELP_TOKEN
    headers = {"Authorization": "bearer %s" % token}
    url = settings.YELP_REST_ENDPOINT + business_id + "/reviews"
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def get_restaurant(business_id):
    if not business_id:
        return None
    response = {
        "restaurant_data": get_restaurant_data(business_id),
        "restaurant_reviews": get_restaurant_reviews(business_id),
    }
    return response


def get_restaurant_list(page, size, sort_property, client_ip):
    if sort_property == "lowestPrice":
        restaurants = Restaurant.objects.order_by("price")
    elif sort_property == "highestPrice":
        restaurants = Restaurant.objects.order_by("-price")
    elif sort_property == "nearest":
        g = GeoIP2()
        try:
            client_position = g.lat_lon(client_ip)
        except:
            client_ip = "207.172.171.222"
            client_position = g.lat_lon(client_ip)
        restaurants = Restaurant.objects.all()
        restaurants = sorted(
            restaurants,
            key=lambda x: math.sqrt(client_position[0] - float(x.latitude))
            + math.sqrt(client_position[1] - float(x.longitude)),
            reverse=False,
        )
    else:
        restaurants = Restaurant.objects.all()
    offset = page * int(size)
    restaurant_list = restaurants[offset : offset + size]
    response = []
    for restaurant in restaurant_list:
        response.append(restaurant.__dict__)

    return response


def get_page_range(total_page, curr_page):
    page_range = []
    lower = max(0, curr_page - 2)
    upper = min(total_page, curr_page + 2)
    if curr_page < 2:
        upper = min(lower + 4, total_page)
    if curr_page > total_page - 2:
        lower = max(0, upper - 4)
    for num in range(lower, upper + 1):
        page_range.append(num)
    return page_range


def get_star_list():
    nums = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    result = {}
    for num in nums:
        full = num - (num % 1)
        half = 1 if num % 1 != 0 else 0
        null = 5 - full - half
        result[num] = [range(int(full)), range(int(half)), range(int(null))]
    return result
