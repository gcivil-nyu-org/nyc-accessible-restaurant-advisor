from django.conf import settings
from django.db.models import Q
from .models import Restaurant
import requests
import json


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


def get_restaurant_list(page, size, restaurants):
    offset = page * int(size)
    restaurants = restaurants[offset : offset + size]
    response = []
    for restaurant in restaurants:
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


def decompose_keyword(keyword):
    """
    @ Return: A context dictionary contains:
     possible keywords list,
     possible zipcodes list
    """
    words = keyword.split(',')
    codes_list, words_list = [], []
    for word in words:
        key = word.strip()
        if len(key) == 0:
            continue
        if key.isdigit() and len(key) == 5:
            codes_list.append(key)
        else:
            words_list.append(key)
    context = {
        'codes_list': codes_list,
        'words_list': words_list,
    }
    print(context)
    return context


def get_search_restaurant(keyword):
    context = decompose_keyword(keyword)
    codes_list = context['codes_list']
    words_list = context['words_list']
    restaurant_list = []
    restaurants = Restaurant.objects.all()
    for word in words_list:
        restaurants = restaurants.filter(Q(name__icontains=word) |
                                         Q(category1__icontains=word) |
                                         Q(category2__icontains=word) |
                                         Q(category3__icontains=word) |
                                         Q(address__icontains=word))

    for zip_code in codes_list:
        restaurants = restaurants.filter(zip_code__contains=zip_code)
    return restaurants
