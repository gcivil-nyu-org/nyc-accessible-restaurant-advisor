from django.conf import settings


from .models import Restaurant, Review, User_Profile, User

from .models import Restaurant, Review, User_Profile, Comment

from django.db.models import Q
from .models import Restaurant
import requests
import json
import math

from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError


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
    """
    @ Return: Dictionary of local reviews of specific restaurant
        Each review also contain a comment list
    """
    if not business_id:
        return None
    target_restaurant = Restaurant.objects.get(business_id=business_id)
    reviews = Review.objects.filter(restaurant=target_restaurant)
    response = []
    for review in reversed(list(reviews)):
        user = review.user
        comments = review.comments.all()
        if user.is_user:
            profile = User_Profile.objects.get(user=user)
            photo = profile.photo
            review.user_id = user.id
            review.username = user.username
            review.photo = photo
            review.comments_set = reversed(list(comments))
            response.append(review.__dict__)
        elif user.is_restaurant:
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


def get_restaurant_list(page, size, sort_property, client_ip, restaurants):
    if sort_property == "lowestPrice":
        restaurants = restaurants.order_by("price")
    elif sort_property == "highestPrice":
        restaurants = restaurants.order_by("-price")
    elif sort_property == "nearest":
        g = GeoIP2()
        try:
            client_position = g.lat_lon(client_ip)
        except AddressNotFoundError:
            client_ip = "207.172.171.222"
            client_position = g.lat_lon(client_ip)
        restaurants = sorted(
            restaurants,
            key=lambda x: (client_position[0] - float(x.latitude)) ** 2
            + (client_position[1] - float(x.longitude)) ** 2,
            reverse=False,
        )

    offset = page * int(size)
    restaurant_list = restaurants[offset : offset + size]

    total_restaurant = len(restaurants)
    restaurants_sublist = []
    for restaurant in restaurant_list:
        restaurants_sublist.append(restaurant.__dict__)
    response = {
        "total_restaurant": total_restaurant,
        "restaurants_list": restaurants_sublist,
    }
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
    words = keyword.split(",")
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
        "codes_list": codes_list,
        "words_list": words_list,
    }
    return context


def get_search_restaurant(keyword):
    context = decompose_keyword(keyword)
    codes_list = context["codes_list"]
    words_list = context["words_list"]

    restaurants = Restaurant.objects.all()
    for word in words_list:
        restaurants = restaurants.filter(
            Q(name__icontains=word)
            | Q(category1__icontains=word)
            | Q(category2__icontains=word)
            | Q(category3__icontains=word)
            | Q(address__icontains=word)
        )

    for zip_code in codes_list:
        restaurants = restaurants.filter(zip_code__contains=zip_code)
    return restaurants


def get_filter_restaurant(filters, restaurants):
    prices = filters["prices"]
    categories = filters["categories"]

    price_flag = False
    categories_flag = False
    for price in prices:
        if price:
            price_flag = True
            break
    for i in range(len(categories)):
        if categories[i]:
            categories_flag = True
        else:
            categories[i] = "#"

    price1, price2, price3, price4 = prices
    chinese, korean, salad, pizza = categories

    if price_flag:

        restaurants = restaurants.filter(
            Q(price=price1) | Q(price=price2) | Q(price=price3) | Q(price=price4)
        )
    if categories_flag:

        restaurants = restaurants.filter(
            Q(category1__icontains=chinese)
            | Q(category2__icontains=chinese)
            | Q(category3__icontains=chinese)
            | Q(category1__icontains=korean)
            | Q(category2__icontains=korean)
            | Q(category3__icontains=korean)
            | Q(category1__icontains=salad)
            | Q(category2__icontains=salad)
            | Q(category3__icontains=salad)
            | Q(category1__icontains=pizza)
            | Q(category2__icontains=pizza)
            | Q(category3__icontains=pizza)
        )
    return restaurants


def get_public_user_detail(user):
    if not user:
        return None
    user_instance = User.objects.get(pk=user)
    if user_instance.is_user:
        response = {
            "username": user_instance.username,
            "email": user_instance.email,
            "first_name": user_instance.first_name,
            "last_name": user_instance.last_name,
            "address": user_instance.uprofile.address,
            "phone": user_instance.uprofile.phone,
            "zip_code": user_instance.uprofile.zip_code,
            "state": user_instance.uprofile.state,
            "city": user_instance.uprofile.city,
            "photo": user_instance.uprofile.photo,
        }
    elif user_instance.is_restaurant:
        response = {}

    return response


def get_user_reviews(user):
    if not user:
        return None
    all_reviews = Review.objects.filter(user=user)
    response = []
    for review in all_reviews:
        restaurant = review.restaurant
        review.business_id = restaurant.business_id
        review.res_name = restaurant.name
        review.res_url = restaurant.img_url
        response.append(review.__dict__)
    return response
