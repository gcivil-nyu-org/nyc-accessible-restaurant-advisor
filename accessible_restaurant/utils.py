from django.conf import settings
from .models import Restaurant, Review, User_Profile
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


def get_local_restaurant_data(business_id):
    # get the accessible rating
    if not business_id:
        return None
    target_restaurant = Restaurant.objects.get(business_id=business_id)
    reviews = Review.objects.filter(restaurant=target_restaurant)
    count = 0
    level_entry_rating = 0
    wide_door_rating = 0
    accessible_table_rating = 0
    accessible_restroom_rating = 0
    accessible_path_rating = 0

    for review in reviews:
        level_entry_rating += review.level_entry_rating
        wide_door_rating += review.wide_door_rating
        accessible_table_rating += review.accessible_table_rating
        accessible_restroom_rating += review.accessible_restroom_rating
        accessible_path_rating += review.accessible_path_rating
        count += 1

    response = {}
    if count == 0:
        response["level_entry_rating"] = 0.0
        response["wide_door_rating"] = 0.0
        response["accessible_table_rating"] = 0.0
        response["accessible_restroom_rating"] = 0.0
        response["accessible_path_rating"] = 0.0
    else:
        response["level_entry_rating"] = (
            int(float(level_entry_rating / count) / 0.5) * 0.5
        )
        response["wide_door_rating"] = int(float(wide_door_rating / count) / 0.5) * 0.5
        response["accessible_table_rating"] = (
            int(float(accessible_table_rating / count) / 0.5) * 0.5
        )
        response["accessible_restroom_rating"] = (
            int(float(accessible_restroom_rating / count) / 0.5) * 0.5
        )
        response["accessible_path_rating"] = (
            int(float(accessible_path_rating / count) / 0.5) * 0.5
        )

    return response


def get_local_restaurant_reviews(business_id):
    if not business_id:
        return None
    target_restaurant = Restaurant.objects.get(business_id=business_id)
    reviews = Review.objects.filter(restaurant=target_restaurant)
    response = []
    for review in reviews:
        user = review.user
        profile = User_Profile.objects.get(user=user)
        photo = profile.photo
        review.username = user.username
        review.photo = photo
        response.append(review.__dict__)
    return response


def get_restaurant(business_id):
    if not business_id:
        return None
    response = {
        "restaurant_data": get_restaurant_data(business_id),
        "restaurant_reviews": get_restaurant_reviews(business_id),
        "local_restaurant_data": get_local_restaurant_data(business_id),
        "local_restaurant_reviews": get_local_restaurant_reviews(business_id),
    }
    return response


def get_restaurant_list(page, size):
    offset = page * int(size)
    restaurants = Restaurant.objects.all()[offset : offset + size]
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
