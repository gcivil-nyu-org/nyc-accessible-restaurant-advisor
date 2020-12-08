from django.conf import settings

from .models import (
    Restaurant,
    Review,
    User_Profile,
    User,
    Favorites,
    User_Preferences,
    Comment,
)

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
            review.auth_status = profile.auth_status
            review.username = user.username
            review.photo = photo
            review.comments_set = reversed(list(comments))
            # additional set for comments, one set can only use once.
            review.comments_set2 = reversed(list(comments))
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
        restaurants = restaurants.order_by("price", "business_id")
    elif sort_property == "highestPrice":
        restaurants = restaurants.order_by("-price", "business_id")
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
    results = Restaurant.objects.none()

    if len(words_list) > 0:
        for word in words_list:
            restaurants_word_filter = restaurants.filter(
                Q(name__icontains=word)
                | Q(category1__icontains=word)
                | Q(category2__icontains=word)
                | Q(category3__icontains=word)
            )
            results |= restaurants_word_filter

        if len(codes_list) > 0:
            for zip_code in codes_list:
                results = results.filter(zip_code__contains=zip_code)
        return results

    else:
        for zip_code in codes_list:
            results = restaurants.filter(zip_code__contains=zip_code)
        return results


def get_filter_restaurant(filters, restaurants):
    prices = filters["prices"]
    categories = filters["categories"]
    compliant = filters["compliant"]

    price_flag = False
    categories_flag = False
    compliant_flag = False
    for price in prices:
        if price:
            price_flag = True
            break
    for i in range(len(categories)):
        if categories[i]:
            categories_flag = True
        else:
            categories[i] = "#"
    if compliant[0] or compliant[1]:
        compliant_flag = True

    price1, price2, price3, price4 = prices
    chinese, korean, salad, pizza, sandwiches, brunch, coffee = categories
    allRestaurants, notCompliant = compliant

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
            | Q(category1__icontains=sandwiches)
            | Q(category2__icontains=sandwiches)
            | Q(category3__icontains=sandwiches)
            | Q(category1__icontains=brunch)
            | Q(category2__icontains=brunch)
            | Q(category3__icontains=brunch)
            | Q(category1__icontains=coffee)
            | Q(category2__icontains=coffee)
            | Q(category3__icontains=coffee)
        )
    if compliant_flag:
        if notCompliant:
            restaurants = restaurants.filter(Q(compliant=False))
    else:
        restaurants = restaurants.filter(Q(compliant=True))
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
        review.comments_count = len(Comment.objects.filter(review=review.id))
        response.append(review.__dict__)
    return response


def get_user_preferences(user):
    if not user:
        return None
    # Get user info and preferences
    user_instance = User.objects.get(pk=user.id)
    if user_instance.is_user:
        user_zip_code = user_instance.uprofile.zip_code
        user_borough = user_instance.uprofile.borough
        all_preferences = User_Preferences.objects.filter(user=user)
        for preference in all_preferences:
            user_dining1 = preference.dining_pref1
            user_dining2 = preference.dining_pref2
            user_dining3 = preference.dining_pref3
            user_budget = preference.budget_pref
            user_location = preference.location_pref
            user_dietary = preference.dietary_pref
            user_cuisine1 = preference.cuisine_pref1
            user_cuisine2 = preference.cuisine_pref2

        # Recommendation Process

        # 1. Limit possibilities to those with reviews above 20
        restaurants = Restaurant.objects.all().filter(review_count__gt=20)

        # 2. Limit possibilities to those with ratings at or above 4
        restaurants = restaurants.filter(rating__gte=4)
        restaurants = restaurants.filter(compliant__exact=True)

        # 3. Rank each restaurant according to user preferences
        ranked_restaurants = {}
        for r in restaurants:
            id = r.business_id
            main_category1 = r.main_category1
            main_category2 = r.main_category2
            main_category3 = r.main_category3
            category1 = r.category1
            category2 = r.category2
            category3 = r.category3
            price = r.price
            borough = r.city
            zip_code = r.zip_code

            score = 0

            all_options = [user_dining1, user_dining2, user_dining3]
            dining_options = []
            for d in all_options:
                if d != "No Preference":
                    dining_options.append(d)

            dining_prefs = list(set(dining_options))
            if main_category1 in dining_prefs:
                score = score + 1
            if main_category2 in dining_prefs:
                score = score + 1
            if main_category3 in dining_prefs:
                score = score + 1

            if user_budget == price:
                score = score + 1

            if (user_location == "Near Home") and (str(user_zip_code) == str(zip_code)):
                score = score + 1
            elif (user_location == "Within My Borough") and (user_borough == borough):
                score = score + 1
            elif (user_location == "Outside My Borough") and (user_borough != borough):
                score = score + 1

            if (
                (user_dietary in category1)
                or (user_dietary in category2)
                or (user_dietary in category3)
            ):
                score = score + 1

            if (
                (user_cuisine1 in category1)
                or (user_cuisine1 in category2)
                or (user_cuisine1 in category3)
            ):
                score = score + 1

            if (
                (user_cuisine2 in category1)
                or (user_cuisine2 in category2)
                or (user_cuisine2 in category3)
            ):
                score = score + 1

            ranked_restaurants[id] = score

        # Sort restaurants by highest score
        ranked_restaurants_sorted = sorted(
            ranked_restaurants.items(), key=lambda x: x[1], reverse=True
        )

        # Get top three restaurants by id
        id1 = ranked_restaurants_sorted[0][0]
        id2 = ranked_restaurants_sorted[1][0]
        id3 = ranked_restaurants_sorted[2][0]

        recommended_restaurants = Restaurant.objects.all().filter(
            Q(business_id__contains=id1)
            | Q(business_id__contains=id2)
            | Q(business_id__contains=id3)
        )
        return recommended_restaurants


def get_user_favorite(user):
    if not user:
        return None
    user_instance = User.objects.get(pk=user)
    all_favorite = Favorites.objects.filter(user=user_instance)
    response = []
    for favorite in all_favorite:
        restaurant = Restaurant.objects.get(pk=favorite.restaurant_id)
        response.append(restaurant.__dict__)
    return response


def get_user_profile_favorite(user):
    if not user:
        return None
    all_favorite = Favorites.objects.filter(user=user)
    response = []
    for favorite in all_favorite:
        restaurant = Restaurant.objects.get(pk=favorite.restaurant_id)
        response.append(restaurant.__dict__)
    return response
