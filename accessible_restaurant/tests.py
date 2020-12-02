from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.test import SimpleTestCase
import accessible_restaurant
import django
from accessible_restaurant.views import (
    index_view_personalized,
    user_profile_view,
    emailsent_view,
    activate_account,
    restaurant_profile_view,
    restaurant_detail_view,
    signup_view,
    UserSignUpView,
    RestaurantSignUpView,
    restaurant_list_view,
)
from django.contrib.auth import views as auth_views
from accessible_restaurant.forms import (
    UserSignUpForm,
    RestaurantSignUpForm,
    UserProfileUpdateForm,
    UserUpdateForm,
    RestaurantProfileUpdateForm,
    ReviewPostForm,
    ContactForm,
    UserCertUpdateForm,
    UserCertVerifyForm,
)

from django.test import TestCase, Client
from django.urls import reverse
from accessible_restaurant.models import (
    User,
    User_Profile,
    Restaurant_Profile,
    Restaurant,
    Review,
    ApprovalPendingUsers,
    ApprovalPendingRestaurants,
)
import json

from django.conf import settings


# Create your tests here.
class TestForms(TestCase):
    def test_userSignUpForm_is_valid(self):
        form = UserSignUpForm(
            data={
                "username": "test1",
                "email": "test@test.com",
                "first_name": "test",
                "last_name": "user",
                "password1": "Password123#",
                "password2": "Password123#",
            }
        )
        self.assertTrue(form.is_valid())

    def test_userSignUpForm_no_data(self):
        form = UserSignUpForm(
            data={
                "username": "test1",
                "email": "test@test.com",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_userSignUpForm_no_data_4(self):
        form = UserSignUpForm(
            data={
                "username": "test1",
                "email": "test@test.com",
                "first_name": "test",
                "last_name": "user",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_RestaurantSignUpForm_is_valid(self):
        form = RestaurantSignUpForm(
            data={
                "username": "test1",
                "email": "test@test.com",
                "password1": "Password123#",
                "password2": "Password123#",
            }
        )
        self.assertTrue(form.is_valid())

    def test_RestaurantSignUpForm_no_data(self):
        form = RestaurantSignUpForm(
            data={
                "username": "test1",
                "email": "test@test.com",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_RestaurantSignUpForm_no_data_4(self):
        form = RestaurantSignUpForm(
            data={
                "username": "test1",
                "email": "test@test.com",
                "first_name": "test",
                "last_name": "user",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_UserProfileUpdateForm_is_valid(self):
        form = UserProfileUpdateForm(
            data={
                "photo": "photo",
                "phone": 1234567889,
                "address": "123 New York",
                "borough": "Brooklyn",
                "city": "New York",
                "Zip Code": 11220,
                "state": "New York",
                "auth_status": "uncertified",
            }
        )
        self.assertTrue(form.is_valid())

    def test_RestaurantProfileUpdateForm_is_valid(self):
        form = RestaurantProfileUpdateForm(
            data={
                "restaurant_name": "Pizza",
                "photo": "Photo",
                "phone": "1234567889",
                "address": "345 NY",
                "city": "Manhattan",
                "zip_code": "11220",
                "state": "NY",
                "is_open": "True",
            }
        )
        self.assertTrue(form.is_valid())

    def test_UserUpdateForm_is_valid(self):
        form = UserUpdateForm(
            data={"username": "testuser", "first_name": "test", "last_name": "user"}
        )
        self.assertTrue(form.is_valid())

    def test_WriteReviewForm_is_valid(self):
        form = ReviewPostForm(
            data={
                "rating": 5,
                "level_entry_rating": 5,
                "wide_door_rating": 5,
                "accessible_table_rating": 5,
                "accessible_restroom_rating": 5,
                "accessible_path_rating": 5,
                "review_context": "test review",
            }
        )
        self.assertTrue(form.is_valid())

    # Supply no file for certification
    def test_UserCertUpdateForm_is_valid(self):
        form = UserCertUpdateForm(data={"auth_documents": "", "auth_status": "pending"})
        self.assertFalse(form.is_valid())

    def test_UserCertVerifyForm_is_valid(self):
        form = UserCertVerifyForm(data={"auth_status": "pending"})
        self.assertTrue(form.is_valid())


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("accessible_restaurant:index")
        # print(resolve(url))
        self.assertEquals(
            resolve(url).func, accessible_restaurant.views.index_view_personalized
        )

    def test_email_sent_url_is_resolved(self):
        url = reverse("accessible_restaurant:emailsent")
        # print(resolve(url))
        self.assertEquals(resolve(url).func, accessible_restaurant.views.emailsent_view)

    def test_user_profile_url_is_resolved(self):
        url = reverse("accessible_restaurant:user_profile")
        # print(resolve(url))
        self.assertEquals(
            resolve(url).func, accessible_restaurant.views.user_profile_view
        )

    def test_restaurant_profile_sent_url_is_resolved(self):
        url = reverse("accessible_restaurant:restaurant_profile")
        # print(resolve(url))
        self.assertEquals(
            resolve(url).func, accessible_restaurant.views.restaurant_profile_view
        )

    def test_login_url_is_resolved(self):
        url = reverse("accessible_restaurant:login")
        # print(resolve(url))
        self.assertEquals(
            resolve(url).func.view_class, django.contrib.auth.views.LoginView
        )

    def test_logout_url_is_resolved(self):
        url = reverse("accessible_restaurant:logout")
        # print(resolve(url))
        self.assertEquals(
            resolve(url).func.view_class, django.contrib.auth.views.LogoutView
        )

    def test_signup_url_is_resolved(self):
        url = reverse("accessible_restaurant:signup")
        # print(resolve(url))
        self.assertEquals(resolve(url).func, accessible_restaurant.views.signup_view)

    def test_user_signup_url_is_resolved(self):
        url = reverse("accessible_restaurant:user_signup")
        # print(resolve(url))
        self.assertEquals(
            resolve(url).func.view_class, accessible_restaurant.views.UserSignUpView
        )

    def test_restaurant_signup_url_is_resolved(self):
        url = reverse("accessible_restaurant:restaurant_signup")
        # print(resolve(url))
        self.assertEquals(
            resolve(url).func.view_class,
            accessible_restaurant.views.RestaurantSignUpView,
        )

    def test_browse_url_is_resolved(self):
        url = reverse("accessible_restaurant:browse", args=["page"])
        # print(resolve(url))
        self.assertEquals(
            resolve(url).func, accessible_restaurant.views.restaurant_list_view
        )

    def test_detail_sent_url_is_resolved(self):
        url = reverse("accessible_restaurant:detail", args=["detail"])
        # print(resolve(url))
        self.assertEquals(
            resolve(url).func, accessible_restaurant.views.restaurant_detail_view
        )

    def test_activate_url_is_resolved(self):
        url = reverse("accessible_restaurant:activate", args=["uidb64", "token"])
        # print(resolve(url))
        self.assertEquals(
            resolve(url).func, accessible_restaurant.views.activate_account
        )

    def test_write_review_url_is_resolved(self):
        url = reverse(
            "accessible_restaurant:write_review", args=["FaPtColHYcTnZAxtoM33cA"]
        )
        self.assertEquals(
            resolve(url).func, accessible_restaurant.views.write_review_view
        )


class UserSignUpTest(TestCase):
    def setUp(self):
        self.usersignup_url = reverse("accessible_restaurant:user_signup")
        self.user = {
            "username": "test",
            "email": "testemail@gmail.com",
            "first_name": "first",
            "last_name": "last",
            "password1": "123456test",
            "password2": "123456test",
        }
        return super().setUp()

    def test_can_view_page_correctly(self):
        response = self.client.get(self.usersignup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/userSignup.html")

    def test_can_register_user(self):
        response = self.client.post(self.usersignup_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "accounts/activate_account.html")


class RestaurantSignUpTest(TestCase):
    def setUp(self):
        self.restaurantsignup_url = reverse("accessible_restaurant:restaurant_signup")
        self.restaurant = {
            "username": "test",
            "email": "testemail@gmail.com",
            "password1": "123456test",
            "password2": "123456test",
        }
        return super().setUp()

    def test_can_view_page_correctly(self):
        response = self.client.get(self.restaurantsignup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/restaurantSignup.html")

    def test_can_register_user(self):
        response = self.client.post(
            self.restaurantsignup_url, self.restaurant, format="text/html", follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/emailSent.html")


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse("accessible_restaurant:index")
        self.about_url = reverse("accessible_restaurant:about")
        self.logout_url = reverse("accessible_restaurant:logout")
        self.about_url = reverse("accessible_restaurant:about")
        self.signup_url = reverse("accessible_restaurant:signup")
        self.emailsent_url = reverse("accessible_restaurant:emailsent")
        self.user_profile_url = reverse("accessible_restaurant:user_profile")
        self.activate_url = reverse(
            "accessible_restaurant:activate", args=["uid", "token"]
        )

        self.userprofile_url = reverse("accessible_restaurant:user_profile")
        self.resprofile_url = reverse("accessible_restaurant:restaurant_profile")
        self.browse_url = reverse("accessible_restaurant:browse", args=[10])
        self.detail_url = reverse(
            "accessible_restaurant:detail", args=["FaPtColHYcTnZAxtoM33cA"]
        )
        self.review_url = reverse(
            "accessible_restaurant:write_review", args=["FaPtColHYcTnZAxtoM33cA"]
        )

    def test_about_view(self):
        response = self.client.get(self.about_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/about.html")

    def test_logout_view(self):
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)
        # self.assertTemplateUsed(response, 'accounts/logout.html')

    def test_index_view_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_logout_view_GET(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_about_view_GET(self):
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/about.html")

    def test_signup_view_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_email_sent_view_GET(self):
        response = self.client.get(self.emailsent_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/emailSent.html")

    # def test_activate_view_GET(self):
    #     # User.objects.create(
    #     #     username="username",
    #     #     first_name="first",
    #     #     last_name="last"
    #     # )
    #     response = self.client.get(self.activate_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "accountss/activate_account.html")

    def test_browse_view_GET(self):
        response = self.client.get(self.browse_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/listing.html")

    def test_detail_view_GET(self):
        Restaurant.objects.create(
            business_id="FaPtColHYcTnZAxtoM33cA",
            name="name",
            img_url="https://i.pinimg.com/originals/4e/24/f5/4e24f523182e09376bfe8424d556610a.png",
            rating="4.5",
            address="50 W 34th street",
            city="New York",
            zip_code="10001",
            phone="3472692389",
            compliant="1",
        )
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/details.html")

    def test_user_profile_view_POST(self):
        self.user = User.objects.create_user(
            "huanjin", "zhanghuanjin97@gmail.com", "test123456"
        )
        # self.client.login(username="huanjin", password="test123456")
        self.user.uprofile = User_Profile.objects.create(
            photo="default.jpg",
            phone="3474223609",
            address="35 River Drive South",
            city="Jersey City",
            zip_code="07310",
            state="NJ",
        )
        response = self.client.post(
            self.userprofile_url,
            {
                "photo": "default.jpg",
                "phone": "3474223609",
                "address": "35 River Drive South",
                "city": "Jersey City",
                "zip_code": "07310",
                "state": "NJ",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.user.uprofile.phone, "3474223609")
        # self.assertTemplateUsed(response, "profile/user_profile.html")

    def test_res_profile_view_POST(self):
        self.user = User.objects.create_user(
            "huanjin", "zhanghuanjin97@gmail.com", "test123456"
        )
        # self.client.login(username="huanjin", password="test123456")
        self.user.rprofile = Restaurant_Profile.objects.create(
            restaurant_name="name",
            photo="default.jpg",
            phone="3474223609",
            address="35 River Drive South",
            city="Jersey City",
            zip_code="07310",
            state="NJ",
            is_open=True,
        )

        response = self.client.post(self.resprofile_url)  # self.user.rprofile)
        self.assertEqual(response.status_code, 302)

    def test_write_review_view_GET(self):
        self.user = User.objects.create_user(
            "huanjin",
            "zhanghuanjin97@gmail.com",
            "test123456",
            is_user=True,
        )
        self.client.login(username="huanjin", password="test123456")

        Restaurant.objects.create(
            business_id="FaPtColHYcTnZAxtoM33cA",
            name="Chu Tea",
            img_url="https://s3-media4.fl.yelpcdn.com/bphoto/05Q6eHDSpXmytCf4JHR7AQ/o.jpg",
            rating="4.0",
            latitude="40.668253",
            longitude="-73.986898",
            address="471 5th Ave",
            city="Brooklyn",
            zip_code="11215",
            phone="+17187881113",
            compliant=True,
            price="$",
            category1="Bubble Tea",
            category2="Poke",
            category3="Juice Bars & Smoothies",
        )
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "review/writeReview.html")

    # def test_review_form_valid_view_GET(self):
    #     self.user = User.objects.create_user(
    #         "huanjin", "zhanghuanjin97@gmail.com", "test123456"
    #     )
    #     self.client.login(username="huanjin", password="test123456")
    #     form_data = {
    #         "rating": 5,
    #         "level_entry_rating": 5,
    #         "wide_door_rating": 5,
    #         "accessible_table_rating": 5,
    #         "accessible_restroom_rating": 5,
    #         "accessible_path_rating": 5,
    #         "review_context": "test review",
    #     }
    #
    #     Restaurant.objects.create(
    #         business_id="FaPtColHYcTnZAxtoM33cA",
    #         name="Chu Tea",
    #         img_url="https://s3-media4.fl.yelpcdn.com/bphoto/05Q6eHDSpXmytCf4JHR7AQ/o.jpg",
    #         rating="4.0",
    #         latitude="40.668253",
    #         longitude="-73.986898",
    #         address="471 5th Ave",
    #         city="Brooklyn",
    #         zip_code="11215",
    #         phone="+17187881113",
    #         compliant=True,
    #         price="$",
    #         category1="Bubble Tea",
    #         category2="Poke",
    #         category3="Juice Bars & Smoothies",
    #     )
    #     response = self.client.post(self.detail_url, form_data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "restaurants/details.html")


class TestRestaurantDetail(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "huanjin",
            "zhanghuanjin97@gmail.com",
            "test123456",
            is_user=True,
            first_name="Huanjin",
            last_name="Zhang",
        )

        self.restaurant = Restaurant.objects.create(
            business_id="De_10VF2CrC2moWaPA81mg",
            name="Just Salad",
            img_url="https://s3-media1.fl.yelpcdn.com/bphoto/xX9UzyMKSao3qfsufH9SnA/o.jpg",
            rating="3.5",
            latitude="40.669429",
            longitude="-73.979494",
            address="252 7th Ave",
            city="Brooklyn",
            zip_code="11215",
            phone="+18666733757",
            compliant=True,
            price="$$",
            category1="Salad",
            category2="Wraps",
            category3="Vegetarian",
        )
        Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            review_date="2020-01-01 00:00:00",
            review_context="test review",
            rating="5",
            level_entry_rating="5",
            wide_door_rating="5",
            accessible_table_rating="5",
            accessible_restroom_rating="5",
            accessible_path_rating="5",
        )

        self.detail_url = reverse(
            "accessible_restaurant:detail", args=["De_10VF2CrC2moWaPA81mg"]
        )

        return super().setUp()

    def test_can_view_restaurant_detail_page_correctly(self):
        # self.client.login(username="huanjin", password="test123456")
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/details.html")


# class SortTest(TestCase):
#     def setUp(self):
#         self.sortbydefault_url = reverse(
#             "accessible_restaurant:browse", args=["0", "default"]
#         )
#         self.sortbylowestprice_url = reverse(
#             "accessible_restaurant:browse", args=["0", "lowestprice"]
#         )
#         self.sortbyhighestprice_url = reverse(
#             "accessible_restaurant:browse", args=["0", "highestprice"]
#         )
#         self.sortbynearest_url = reverse(
#             "accessible_restaurant:browse", args=["0", "nearest"]
#         )
#         return super().setUp()
#
#     def test_can_view_page_correctly(self):
#         sortbydefault_response = self.client.get(self.sortbydefault_url)
#         sortbylowestprice_response = self.client.get(self.sortbylowestprice_url)
#         sortbyhighestprice_response = self.client.get(self.sortbyhighestprice_url)
#         sortbynearest_response = self.client.get(self.sortbynearest_url)
#         self.assertEqual(sortbydefault_response.status_code, 200)
#         self.assertEqual(sortbylowestprice_response.status_code, 200)
#         self.assertEqual(sortbyhighestprice_response.status_code, 200)
#         self.assertEqual(sortbynearest_response.status_code, 200)
#         self.assertTemplateUsed(sortbydefault_response, "restaurants/listing.html")
#         self.assertTemplateUsed(sortbylowestprice_response, "restaurants/listing.html")
#         self.assertTemplateUsed(sortbyhighestprice_response, "restaurants/listing.html")
#         self.assertTemplateUsed(sortbynearest_response, "restaurants/listing.html")


class SearchTest(TestCase):
    def setUp(self) -> None:
        Restaurant.objects.create(
            business_id="FaPtColHYcTnZAxtoM33cA",
            name="Chu Tea",
            img_url="https://s3-media4.fl.yelpcdn.com/bphoto/05Q6eHDSpXmytCf4JHR7AQ/o.jpg",
            rating="4.0",
            latitude="40.668253",
            longitude="-73.986898",
            address="471 5th Ave",
            city="Brooklyn",
            zip_code="11215",
            phone="+17187881113",
            compliant=True,
            price="$",
            category1="Bubble Tea",
            category2="Poke",
            category3="Juice Bars & Smoothies",
        )

        Restaurant.objects.create(
            business_id="De_10VF2CrC2moWaPA81mg",
            name="Just Salad",
            img_url="https://s3-media1.fl.yelpcdn.com/bphoto/xX9UzyMKSao3qfsufH9SnA/o.jpg",
            rating="3.5",
            latitude="40.669429",
            longitude="-73.979494",
            address="252 7th Ave",
            city="Brooklyn",
            zip_code="11215",
            phone="+18666733757",
            compliant=True,
            price="$$",
            category1="Salad",
            category2="Wraps",
            category3="Vegetarian",
        )

        self.search_url = reverse("accessible_restaurant:browse", args=["0"])
        self.filter_url = reverse("accessible_restaurant:browse", args=["0"])

    def test_can_view_page_correctly(self):
        response_search_zipcode = self.client.get(self.search_url, {"query": "11215"})
        response_search_restaurant_name = self.client.get(
            self.search_url, {"query": "Chu Tea"}
        )
        response_search_category = self.client.get(
            self.search_url, {"query": "Bubble Tea"}
        )
        response_search_address = self.client.get(self.search_url, {"query": "5th Ave"})
        response_search_multicondition = self.client.get(
            self.search_url, {"query": "11215, Juice Bars"}
        )

        response_filter_price = self.client.get(self.filter_url, {"price1": "$"})
        response_filter_category = self.client.get(self.filter_url, {"Salad": "Salad"})

        self.assertEqual(response_search_zipcode.status_code, 200)
        self.assertEqual(response_search_restaurant_name.status_code, 200)
        self.assertEqual(response_search_category.status_code, 200)
        self.assertEqual(response_search_address.status_code, 200)
        self.assertEqual(response_search_multicondition.status_code, 200)

        self.assertEqual(response_filter_price.status_code, 200)
        self.assertEqual(response_filter_category.status_code, 200)

        self.assertTemplateUsed(response_search_zipcode, "restaurants/listing.html")
        self.assertTemplateUsed(
            response_search_restaurant_name, "restaurants/listing.html"
        )
        self.assertTemplateUsed(response_search_category, "restaurants/listing.html")
        self.assertTemplateUsed(response_search_address, "restaurants/listing.html")
        self.assertTemplateUsed(
            response_search_multicondition, "restaurants/listing.html"
        )

        self.assertTemplateUsed(response_filter_price, "restaurants/listing.html")
        self.assertTemplateUsed(response_filter_category, "restaurants/listing.html")


class FilterTest(TestCase):
    def setUp(self) -> None:
        Restaurant.objects.create(
            business_id="jkl1ukPtVM2UZqMLSJdWFw",
            name="Greenwich Steakhouse",
            img_url="https://s3-media2.fl.yelpcdn.com/bphoto/uN7IpkwZrL7f2jYXbHPDIA/o.jpg",
            rating="4.5",
            latitude="40.73608",
            longitude="-74.00058",
            address="62 Greenwich Ave",
            city="New York",
            zip_code="10011",
            compliant=False,
            price="$$$$",
            category1="Steakhouses",
            category2="Seafood",
            category3="Cocktail Bars",
        )

        Restaurant.objects.create(
            business_id="zuD-iB7hV_dnf_JzBk_DCQ",
            name="Juku",
            img_url="https://s3-media3.fl.yelpcdn.com/bphoto/y1sYBIZzPgPFot9OZeKV8Q/o.jpg",
            rating="4",
            latitude="40.71461",
            longitude="-73.999528",
            address="32 Mulberry St",
            city="New York",
            zip_code="10013",
            phone="16465902111",
            compliant=True,
            price="$$$",
            category1="Sushi Bars",
            category2="Izakaya",
            category3="Cocktail Bars",
        )

        Restaurant.objects.create(
            business_id="4h4Tuuc56YPO6lWfZ1bdSQ",
            name="Joe's Pizza",
            img_url="https://s3-media3.fl.yelpcdn.com/bphoto/iiFPnKfxI2_UjJHbCd2iCQ/o.jpg",
            rating="4",
            latitude="40.71012977",
            longitude="-74.00772069",
            address="124 Fulton St",
            city="New York",
            zip_code="10038",
            phone="12122670860",
            compliant=True,
            price="$",
            category1="Pizza",
        )

        self.filter_url = reverse("accessible_restaurant:browse", args=["0"])

    def test_individual_filter_price(self):

        response_filter_most_expensive = self.client.get(
            self.filter_url, {"price4": "$$$$"}
        )
        response_filter_less_expensive = self.client.get(
            self.filter_url, {"price3": "$$$"}
        )
        response_filter_least_expensive = self.client.get(
            self.filter_url, {"price1": "$"}
        )

        string_most_expensive = response_filter_most_expensive.content.decode(
            encoding="UTF-8"
        )
        string_less_expensive = response_filter_less_expensive.content.decode(
            encoding="UTF-8"
        )
        string_least_expensive = response_filter_least_expensive.content.decode(
            encoding="UTF-8"
        )

        self.assertEqual(response_filter_most_expensive.status_code, 200)
        self.assertEqual(response_filter_less_expensive.status_code, 200)
        self.assertEqual(response_filter_least_expensive.status_code, 200)

        self.assertIn(
            "jkl1ukPtVM2UZqMLSJdWFw", string_most_expensive
        )  # Greenwich Steakhouse
        self.assertNotIn("zuD-iB7hV_dnf_JzBk_DCQ", string_most_expensive)  # Juku
        self.assertNotIn("4h4Tuuc56YPO6lWfZ1bdSQ", string_most_expensive)  # Joe's Pizza

        self.assertIn("zuD-iB7hV_dnf_JzBk_DCQ", string_less_expensive)  # Juku
        self.assertNotIn(
            "jkl1ukPtVM2UZqMLSJdWFw", string_less_expensive
        )  # Greenwich Steakhouse
        self.assertNotIn("4h4Tuuc56YPO6lWfZ1bdSQ", string_less_expensive)  # Joe's Pizza

        self.assertIn("4h4Tuuc56YPO6lWfZ1bdSQ", string_least_expensive)  # Joe's Pizza
        self.assertNotIn(
            "jkl1ukPtVM2UZqMLSJdWFw", string_least_expensive
        )  # Greenwich Steakhouse
        self.assertNotIn("zuD-iB7hV_dnf_JzBk_DCQ", string_least_expensive)  # Juku

    def test_group_filter_price(self):

        response_filter_more_expensive = self.client.get(
            self.filter_url, {"price4": "$$$$", "price3": "$$$"}
        )
        response_filter_less_expensive = self.client.get(
            self.filter_url, {"price3": "$$$", "price1": "$"}
        )
        response_filter_all = self.client.get(
            self.filter_url, {"price1": "$", "price3": "$$$", "price4": "$$$$"}
        )

        string_more_expensive = response_filter_more_expensive.content.decode(
            encoding="UTF-8"
        )
        string_less_expensive = response_filter_less_expensive.content.decode(
            encoding="UTF-8"
        )
        string_all = response_filter_all.content.decode(encoding="UTF-8")

        self.assertEqual(response_filter_more_expensive.status_code, 200)
        self.assertEqual(response_filter_less_expensive.status_code, 200)
        self.assertEqual(response_filter_all.status_code, 200)

        self.assertIn(
            "jkl1ukPtVM2UZqMLSJdWFw", string_more_expensive
        )  # Greenwich Steakhouse
        self.assertIn("zuD-iB7hV_dnf_JzBk_DCQ", string_more_expensive)  # Juku
        self.assertNotIn("4h4Tuuc56YPO6lWfZ1bdSQ", string_more_expensive)  # Joe's Pizza

        self.assertNotIn(
            "jkl1ukPtVM2UZqMLSJdWFw", string_less_expensive
        )  # Greenwich Steakhouse
        self.assertIn("zuD-iB7hV_dnf_JzBk_DCQ", string_less_expensive)  # Juku
        self.assertIn("4h4Tuuc56YPO6lWfZ1bdSQ", string_less_expensive)  # Joe's Pizza

        self.assertIn("jkl1ukPtVM2UZqMLSJdWFw", string_all)  # Greenwich Steakhouse
        self.assertIn("zuD-iB7hV_dnf_JzBk_DCQ", string_all)  # Juku
        self.assertIn("4h4Tuuc56YPO6lWfZ1bdSQ", string_all)  # Joe's Pizza

    def test_category_filter(self):

        response_filter_category = self.client.get(self.filter_url, {"Pizza": "Pizza"})

        string_response = response_filter_category.content.decode(encoding="UTF-8")

        self.assertEqual(response_filter_category.status_code, 200)

        self.assertNotIn(
            "jkl1ukPtVM2UZqMLSJdWFw", string_response
        )  # Greenwich Steakhouse
        self.assertNotIn("zuD-iB7hV_dnf_JzBk_DCQ", string_response)  # Juku
        self.assertIn("4h4Tuuc56YPO6lWfZ1bdSQ", string_response)  # Joe's Pizza

        self.assertNotIn(
            "jkl1ukPtVM2UZqMLSJdWFw", string_response
        )  # Greenwich Steakhouse
        self.assertNotIn("zuD-iB7hV_dnf_JzBk_DCQ", string_response)  # Juku
        self.assertIn("4h4Tuuc56YPO6lWfZ1bdSQ", string_response)  # Joe's Pizza


class TestModels(TestCase):
    def test_save_restaurant_profile_image_correctly(self):
        self.user = User.objects.create_user(
            "huanjin", "zhanghuanjin97@gmail.com", "test123456"
        )
        # self.client.login(username="huanjin", password="test123456")
        self.user.rprofile = Restaurant_Profile.objects.create(
            restaurant_name="name",
            photo="default.jpg",
            phone="3474223609",
            address="35 River Drive South",
            city="Jersey City",
            zip_code="07310",
            state="NJ",
            is_open=True,
        )

        self.assertEquals(self.user.rprofile.photo.height, 300)
        self.assertEquals(self.user.rprofile.photo.width, 300)
        self.assertEqual(str(self.user.rprofile), "huanjin Restaurant Profile")
        # self.assertEquals(self.user.rprofile.photo.path , "\media\default.jpg")

    def test_ApprovalPendingUsers_correctly(self):
        self.user = User.objects.create_user(
            "huanjin", "zhanghuanjin97@gmail.com", "test123456"
        )

        self.user.auth = ApprovalPendingUsers.objects.create(
            auth_documents="documents/pdfs/test.pdf",
            auth_status="N/A",
            time_created="",
        )

    def test_save_user_profile_image_correctly(self):
        self.user = User.objects.create_user(
            "huanjin", "zhanghuanjin97@gmail.com", "test123456"
        )

        # self.client.login(username="huanjin", password="test123456")
        self.user.uprofile = User_Profile.objects.create(
            photo="default.jpg",
            phone="3474223609",
            address="35 River Drive South",
            city="Jersey City",
            zip_code="07310",
            state="NJ",
        )
        self.assertEquals(self.user.uprofile.photo.height, 300)
        self.assertEquals(self.user.uprofile.photo.width, 300)

        self.assertEqual(str(self.user.uprofile), "huanjin User Profile")

    def test_review_model_correctly(self):
        self.user = User.objects.create_user(
            "huanjin", "zhanghuanjin97@gmail.com", "test123456"
        )
        self.client.login(username="huanjin", password="test123456")

        self.Restaurant = Restaurant.objects.create(
            business_id="FaPtColHYcTnZAxtoM33cA",
            name="Chu Tea",
            img_url="https://s3-media4.fl.yelpcdn.com/bphoto/05Q6eHDSpXmytCf4JHR7AQ/o.jpg",
            rating="4.0",
            latitude="40.668253",
            longitude="-73.986898",
            address="471 5th Ave",
            city="Brooklyn",
            zip_code="11215",
            phone="+17187881113",
            compliant=True,
            price="$",
            category1="Bubble Tea",
            category2="Poke",
            category3="Juice Bars & Smoothies",
        )
        self.Review = Review.objects.create(
            user=self.user,
            restaurant=self.Restaurant,
            review_date="2020-05-01",
            rating=5,
            level_entry_rating=5,
            wide_door_rating=5,
            accessible_table_rating=5,
            accessible_restroom_rating=5,
            accessible_path_rating=5,
            review_context="test review",
        )
        self.assertEqual(str(self.Review), "huanjin review on Chu Tea")

    def test_save_restaurant_name_correctly(self):
        self.Restaurant = Restaurant.objects.create(
            business_id="De_10VF2CrC2moWaPA81mg",
            name="Just Salad",
            img_url="https://s3-media1.fl.yelpcdn.com/bphoto/xX9UzyMKSao3qfsufH9SnA/o.jpg",
            rating="3.5",
            latitude="40.669429",
            longitude="-73.979494",
            address="252 7th Ave",
            city="Brooklyn",
            zip_code="11215",
            phone="+18666733757",
            compliant=True,
            price="$$",
            category1="Salad",
            category2="Wraps",
            category3="Vegetarian",
        )

        self.assertEqual(str(self.Restaurant), "Just Salad")


class TestManageCertificate(TestCase):
    def setUp(self):
        # set up three urls
        self.user_profile_url = reverse("accessible_restaurant:user_profile")
        self.restaurant_profile_url = reverse(
            "accessible_restaurant:restaurant_profile"
        )
        self.management_url = reverse("accessible_restaurant:authenticate")

        self.client = Client()

        # create three types of user accounts
        self.super_user = User.objects.create_superuser(
            "admin", "shonna.x.tang@gmail.com", "accessible"
        )
        self.normal_user_1 = User.objects.create_user(
            username="normal_user_1",
            email="shonna.x.tang@gmail.com",
            password="123456test",
            is_user=True,
        )
        self.normal_user_2 = User.objects.create_user(
            username="normal_user_2",
            email="shonna.x.tang@gmail.com",
            password="123456test",
            is_user=True,
        )
        self.restaurant_user = User.objects.create_user(
            username="rest_user",
            email="shonna.x.tang@gmail.com",
            password="123456test",
            is_restaurant=True,
        )

        # create two restaurants
        self.Restaurant1 = Restaurant.objects.create(
            business_id="De_10VF2CrC2moWaPA81mg",
            name="Just Salad",
            img_url="https://s3-media1.fl.yelpcdn.com/bphoto/xX9UzyMKSao3qfsufH9SnA/o.jpg",
            rating="3.5",
            latitude="40.669429",
            longitude="-73.979494",
            address="252 7th Ave",
            city="Brooklyn",
            zip_code="11215",
            phone="+18666733757",
            compliant=True,
            price="$$",
            category1="Salad",
            category2="Wraps",
            category3="Vegetarian",
        )

        self.Restaurant2 = Restaurant.objects.create(
            business_id="FaPtColHYcTnZAxtoM33cA",
            name="Chu Tea",
            img_url="https://s3-media4.fl.yelpcdn.com/bphoto/05Q6eHDSpXmytCf4JHR7AQ/o.jpg",
            rating="4.0",
            latitude="40.668253",
            longitude="-73.986898",
            address="471 5th Ave",
            city="Brooklyn",
            zip_code="11215",
            phone="+17187881113",
            compliant=True,
            price="$",
            category1="Bubble Tea",
            category2="Poke",
            category3="Juice Bars & Smoothies",
        )

        # set up test file path
        self.certificate_file = settings.MEDIA_ROOT + "/documents/pdfs/test.pdf"

        return super().setUp()

    def test_can_upload_and_manage_certificate_correctly(self):
        # Admin can view the manage page correctly
        self.client.login(username="admin", password="accessible")
        management_response = self.client.get(self.management_url)
        self.assertEqual(management_response.status_code, 200)
        self.assertTemplateUsed(management_response, "admin/manage.html")
        self.client.logout()

        # Check authentication request in models
        user_auth_request = ApprovalPendingUsers.objects.all()
        self.assertEqual(len(user_auth_request), 0)
        restaurant_auth_request = ApprovalPendingRestaurants.objects.all()
        self.assertEqual(len(restaurant_auth_request), 0)

        # User upload disability certificate
        self.client.login(username="normal_user_1", password="123456test")
        with open(self.certificate_file, "rb") as fp:
            upload_user_form_data_1 = {
                "submit-certificate": True,
                "auth_documents": fp,
                "auth_status": "pending",
            }
            user_upload_certificate_response_1 = self.client.post(
                self.user_profile_url,
                upload_user_form_data_1,
                HTTP_ACCEPT="application/json",
            )
        self.assertEqual(user_upload_certificate_response_1.status_code, 302)
        self.assertEqual(
            user_upload_certificate_response_1.url, "/accounts/user-profile/"
        )
        self.assertEqual(
            User_Profile.objects.get(user=self.normal_user_1).auth_status, "pending"
        )
        self.client.logout()

        self.client.login(username="normal_user_2", password="123456test")
        with open(self.certificate_file, "rb") as fp:
            upload_user_form_data_2 = {
                "submit-certificate": True,
                "auth_documents": fp,
                "auth_status": "pending",
            }
            user_upload_certificate_response_2 = self.client.post(
                self.user_profile_url,
                upload_user_form_data_2,
                HTTP_ACCEPT="application/json",
            )
        self.assertEqual(user_upload_certificate_response_2.status_code, 302)
        self.assertEqual(
            user_upload_certificate_response_2.url, "/accounts/user-profile/"
        )
        self.assertEqual(
            User_Profile.objects.get(user=self.normal_user_2).auth_status, "pending"
        )
        self.client.logout()

        # Restaurant owner upload business license of the restaurant
        self.client.login(username="rest_user", password="123456test")
        with open(self.certificate_file, "rb") as fp:
            upload_restaurant_form_data_1 = {
                "submit-certificate": True,
                "auth_documents": fp,
                "restaurant": self.Restaurant1.id,
            }
            restaurant_upload_certificate_response_1 = self.client.post(
                self.restaurant_profile_url,
                upload_restaurant_form_data_1,
                HTTP_ACCEPT="application/json",
            )
        self.assertEqual(restaurant_upload_certificate_response_1.status_code, 302)
        self.assertEqual(
            restaurant_upload_certificate_response_1.url,
            "/accounts/restaurant-profile/",
        )

        with open(self.certificate_file, "rb") as fp:
            upload_restaurant_form_data_2 = {
                "submit-certificate": True,
                "auth_documents": fp,
                "restaurant": self.Restaurant2.id,
            }
            restaurant_upload_certificate_response_2 = self.client.post(
                self.restaurant_profile_url,
                upload_restaurant_form_data_2,
                HTTP_ACCEPT="application/json",
            )
        self.assertEqual(restaurant_upload_certificate_response_2.status_code, 302)
        self.assertEqual(
            restaurant_upload_certificate_response_2.url,
            "/accounts/restaurant-profile/",
        )
        self.client.logout()

        # Admin check the user certificate ans restaurant business license
        self.client.login(username="admin", password="accessible")
        management_response = self.client.get(self.management_url)
        self.assertEqual(management_response.status_code, 200)
        self.assertTemplateUsed(management_response, "admin/manage.html")

        # Check authentication request in models
        user_auth_request = ApprovalPendingUsers.objects.all()
        self.assertEqual(len(user_auth_request), 2)
        restaurant_auth_request = ApprovalPendingRestaurants.objects.all()
        self.assertEqual(len(restaurant_auth_request), 2)

        # Admin approve the user certificate
        manage_user_form_data_1 = {
            "submit-user": True,
            "user_id": self.normal_user_1.id,
            "auth_status": "approve",
        }
        admin_approve_user_response = self.client.post(
            self.management_url, manage_user_form_data_1, HTTP_ACCEPT="application/json"
        )
        self.assertEqual(admin_approve_user_response.status_code, 302)
        self.assertEqual(admin_approve_user_response.url, "/manage/")
        normal_user_1_auth_status = User_Profile.objects.get(
            user=self.normal_user_1
        ).auth_status
        self.assertEqual(normal_user_1_auth_status, "certified")

        # Admin approve the restaurant business license
        manage_restaurant_form_data_1 = {
            "submit-restaurant": True,
            "owner_id": self.restaurant_user.id,
            "restaurant_id": self.Restaurant1.business_id,
            "auth_status": "approve",
        }
        admin_approve_restaurant_response = self.client.post(
            self.management_url,
            manage_restaurant_form_data_1,
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(admin_approve_restaurant_response.status_code, 302)
        self.assertEqual(admin_approve_restaurant_response.url, "/manage/")
        restaurant_owner = Restaurant.objects.get(
            business_id=self.Restaurant1.business_id
        ).user
        self.assertEqual(self.restaurant_user, restaurant_owner)

        # Admin disapprove the user certificate
        manage_user_form_data_2 = {
            "submit-user": True,
            "user_id": self.normal_user_2.id,
            "auth_status": "disapprove",
        }
        admin_disapprove_user_response = self.client.post(
            self.management_url, manage_user_form_data_2, HTTP_ACCEPT="application/json"
        )
        self.assertEqual(admin_disapprove_user_response.status_code, 302)
        self.assertEqual(admin_disapprove_user_response.url, "/manage/")
        normal_user_2_auth_status = User_Profile.objects.get(
            user=self.normal_user_2
        ).auth_status
        self.assertEqual(normal_user_2_auth_status, "uncertified")

        # Admin disapprove the restaurant business license
        manage_restaurant_form_data_2 = {
            "submit-restaurant": True,
            "owner_id": self.restaurant_user.id,
            "restaurant_id": self.Restaurant2.business_id,
            "auth_status": "disapprove",
        }
        admin_disapprove_restaurant_response = self.client.post(
            self.management_url,
            manage_restaurant_form_data_2,
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(admin_disapprove_restaurant_response.status_code, 302)
        self.assertEqual(admin_disapprove_restaurant_response.url, "/manage/")
        restaurant_owner = Restaurant.objects.get(
            business_id=self.Restaurant2.business_id
        ).user
        self.assertNotEquals(self.restaurant_user, restaurant_owner)
        self.client.logout()

        # Check to make sure user1 is now certified
        self.client.login(username="normal_user_1", password="123456test")
        self.assertEqual(
            User_Profile.objects.get(user=self.normal_user_1).auth_status, "certified"
        )
        self.client.logout()

        # Check to make sure user2 is now certified
        self.client.login(username="normal_user_2", password="123456test")
        self.assertEqual(
            User_Profile.objects.get(user=self.normal_user_2).auth_status, "uncertified"
        )
        self.client.logout()


class TestPublicFacing(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "huanjin",
            "zhanghuanjin97@gmail.com",
            "test123456",
            is_user=True,
            first_name="Huanjin",
            last_name="Zhang",
        )
        self.user2 = User.objects.create_user(
            "huanjin2",
            "hz2169@nyu.edu",
            "test123456",
            is_restaurant=True,
            first_name="Huanjin",
            last_name="Zhang",
        )
        User_Profile.objects.create(
            photo="default.jpg",
            phone="3474223609",
            address="35 River Drive South",
            city="Jersey City",
            zip_code="07310",
            state="NJ",
            auth_status="uncertified",
        )

        self.restaurant = Restaurant.objects.create(
            business_id="De_10VF2CrC2moWaPA81mg",
            name="Just Salad",
            img_url="https://s3-media1.fl.yelpcdn.com/bphoto/xX9UzyMKSao3qfsufH9SnA/o.jpg",
            rating="3.5",
            latitude="40.669429",
            longitude="-73.979494",
            address="252 7th Ave",
            city="Brooklyn",
            zip_code="11215",
            phone="+18666733757",
            compliant=True,
            price="$$",
            category1="Salad",
            category2="Wraps",
            category3="Vegetarian",
        )
        Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            review_date="2020-01-01 00:00:00",
            review_context="test review",
            rating="5",
            level_entry_rating="5",
            wide_door_rating="5",
            accessible_table_rating="5",
            accessible_restroom_rating="5",
            accessible_path_rating="5",
        )

        self.publicface_isuser_url = reverse(
            "accessible_restaurant:public_facing", args=[self.user.id]
        )
        self.publicface_isres_url = reverse(
            "accessible_restaurant:public_facing", args=[self.user2.id]
        )
        return super().setUp()

    def test_can_view_public_facing_page_correctly(self):
        # self.client.login(username="huanjin", password="test123456")
        isuser_response = self.client.get(self.publicface_isuser_url)
        isres_response = self.client.get(self.publicface_isres_url)
        self.assertEqual(isres_response.status_code, 200)
        self.assertEqual(isuser_response.status_code, 200)
        self.assertTemplateUsed(isuser_response, "publicface/public_profile.html")


class TestFaqContact(TestCase):
    def setUp(self):
        self.faq_url = reverse("accessible_restaurant:faq")
        return super().setUp()

    def test_can_view_faq_page(self):
        form_data = {
            "Email": "zhanghuanjin97@gmail.com",
            "Subject": "Test Subject",
            "Message": "Test Message",
        }
        form = ContactForm(form_data)
        self.assertTrue(form.is_valid())
        get_response = self.client.get(self.faq_url)
        post_response = self.client.post(self.faq_url)
        self.assertEqual(post_response.status_code, 200)
        self.assertTemplateUsed(post_response, "faq/faq_contact.html")
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, "faq/faq_contact.html")


class TestComment(TestCase):
    def setUp(self):
        self.client = Client()

        # three user accounts for testing
        self.user1 = User.objects.create_user(
            username="user1",
            email="xc.test1@gmail.com",
            password="xc1379test",
            is_user=True,
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="xc.test2@gmail.com",
            password="xc1379test",
            is_user=True,
        )
        self.rest_user1 = User.objects.create_user(
            username="rest_user1",
            email="xc.rest1@gmail.com",
            password="xc1379test",
            is_restaurant=True,
        )
        self.rest_user2 = User.objects.create_user(
            username="rest_user2",
            email="xc.rest2@gmail.com",
            password="xc1379test",
            is_restaurant=True,
        )

        # three restaurant for testing
        self.restaurant1 = Restaurant.objects.create(
            business_id="jkl1ukPtVM2UZqMLSJdWFw",
            name="Greenwich Steakhouse",
            img_url="https://s3-media2.fl.yelpcdn.com/bphoto/uN7IpkwZrL7f2jYXbHPDIA/o.jpg",
            rating="4.5",
            latitude="40.73608",
            longitude="-74.00058",
            address="62 Greenwich Ave",
            city="New York",
            zip_code="10011",
            compliant=False,
            price="$$$$",
            category1="Steakhouses",
            category2="Seafood",
            category3="Cocktail Bars",
        )

        self.restaurant2 = Restaurant.objects.create(
            user=self.rest_user2,
            business_id="zuD-iB7hV_dnf_JzBk_DCQ",
            name="Juku",
            img_url="https://s3-media3.fl.yelpcdn.com/bphoto/y1sYBIZzPgPFot9OZeKV8Q/o.jpg",
            rating="4",
            latitude="40.71461",
            longitude="-73.999528",
            address="32 Mulberry St",
            city="New York",
            zip_code="10013",
            phone="16465902111",
            compliant=True,
            price="$$$",
            category1="Sushi Bars",
            category2="Izakaya",
            category3="Cocktail Bars",
        )

        self.restaurant3 = Restaurant.objects.create(
            business_id="4h4Tuuc56YPO6lWfZ1bdSQ",
            name="Joe's Pizza",
            img_url="https://s3-media3.fl.yelpcdn.com/bphoto/iiFPnKfxI2_UjJHbCd2iCQ/o.jpg",
            rating="4",
            latitude="40.71012977",
            longitude="-74.00772069",
            address="124 Fulton St",
            city="New York",
            zip_code="10038",
            phone="12122670860",
            compliant=True,
            price="$",
            category1="Pizza",
        )

        self.restaurant1_url = reverse(
            "accessible_restaurant:detail", args=["jkl1ukPtVM2UZqMLSJdWFw"]
        )
        self.restaurant2_url = reverse(
            "accessible_restaurant:detail", args=["iB7hV_dnf_JzBk_DCQ"]
        )
        self.restaurant3_url = reverse(
            "accessible_restaurant:detail", args=["4h4Tuuc56YPO6lWfZ1bdSQ"]
        )

    def test_review_and_comments(self):
        self.client.login(username="user1", password="xc1379test")

        # user can view the review adding page correctly
        self.review_add_url = reverse(
            "accessible_restaurant:write_review", args=["jkl1ukPtVM2UZqMLSJdWFw"]
        )
        response_view_add_review = self.client.get(self.review_add_url)
        self.assertEqual(response_view_add_review.status_code, 200)
        self.assertTemplateUsed(response_view_add_review, "review/writeReview.html")

        # create a test review form
        form_review_data = {
            "rating": 5,
            "level_entry_rating": 5,
            "wide_door_rating": 5,
            "accessible_table_rating": 5,
            "accessible_restroom_rating": 5,
            "accessible_path_rating": 5,
            "review_context": "test adding review",
        }
        response_add_review = self.client.get(
            self.review_add_url,
            form_review_data,
            # HTTP_ACCEPT='application/json',
        )
        self.assertEqual(response_add_review.status_code, 302)
        self.assertEqual(
            response_add_review.url, "/restaurants/detail/jkl1ukPtVM2UZqMLSJdWFw"
        )
        self.assertEqual(
            Review.objects.get(user=self.user1, restaurant=self.restaurant1).rating, 5
        )
        self.client.logout()

        # create new test review for testing comment
        review1 = Review.objects.create(
            user=self.user2,
            restaurant=self.restaurant2,
            review_context="review for testing comment",
            rating="5",
            level_entry_rating="5",
            wide_door_rating="5",
            accessible_table_rating="5",
            accessible_restroom_rating="5",
            accessible_path_rating="5",
        )

        # test adding comments
        self.assertEqual(len(review1.comments.all()), 0)
        self.comment_add_url = reverse(
            "accessible_restaurant:add_comment",
            args=["zuD-iB7hV_dnf_JzBk_DCQ", review1.id],
        )
        form_add_comment = {"text": "test adding comment"}

        # test adding comment as restaurant user that
        # does not own this restaurant
        self.client.login(username="rest_user1", password="xc1379test")
        response_add_comment_1 = self.client.post(
            self.comment_add_url,
            form_add_comment,
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(len(review1.comments.all()), 0)
        self.assertEqual(response_add_comment_1.status_code, 302)
        self.assertEqual(
            response_add_comment_1.url, "/restaurants/detail/zuD-iB7hV_dnf_JzBk_DCQ"
        )
        self.client.logout()

        self.client.login(username="user1", password="xc1379test")
        response_add_comment_2 = self.client.post(
            self.comment_add_url,
            form_add_comment,
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(len(review1.comments.all()), 1)
        self.assertEqual(response_add_comment_2.status_code, 302)
        self.assertEqual(
            response_add_comment_2.url, "/restaurants/detail/zuD-iB7hV_dnf_JzBk_DCQ"
        )
        self.client.logout()


class TestReview(TestCase):
    def setUp(self):
        # set up two urls
        self.user_profile_url = reverse("accessible_restaurant:user_profile")
        self.restaurant_profile_url = reverse(
            "accessible_restaurant:restaurant_profile"
        )

        self.client = Client()

        # create two types of user accounts
        self.normal_user = User.objects.create_user(
            username="normal_user",
            email="test@test.com",
            password="123456test",
            is_user=True,
        )
        self.restaurant_user = User.objects.create_user(
            username="rest_user",
            email="test@test.com",
            password="123456test",
            is_restaurant=True,
        )

        # set up test image path
        self.image_file = settings.MEDIA_ROOT + "/default.jpg"

        return super().setUp()

    def test_user_can_view_profile_correctly(self):
        self.client.login(username="normal_user", password="123456test")
        user_profile_response = self.client.get(
            "%s?action=View+Profile" % self.user_profile_url
        )
        self.assertEqual(user_profile_response.status_code, 200)
        self.assertTemplateUsed(user_profile_response, "profile/user_profile.html")
        self.client.logout()

    def test_user_can_edit_profile_correctly(self):
        self.client.login(username="normal_user", password="123456test")
        user_profile_response = self.client.get(
            "%s?action=Edit+Profile" % self.user_profile_url
        )
        self.assertEqual(user_profile_response.status_code, 200)
        self.assertTemplateUsed(user_profile_response, "profile/user_profile.html")

        # User edit profile content
        with open(self.image_file, "rb") as fp:
            upload_user_form_data = {
                "submit-info": True,
                "username": "normal_user",
                "first_name": "Normal",
                "last_name": "User",
                "photo": fp,
                "phone": "1234567890",
                "address": "6 Metrotech",
                "borough": "Brooklyn",
                "city": "Brooklyn",
                "zip_code": "11201",
                "state": "New York",
                "auth_status": "uncertified",
            }
            user_update_profile_response = self.client.post(
                self.user_profile_url,
                upload_user_form_data,
                HTTP_ACCEPT="application/json",
            )
        self.assertEqual(user_update_profile_response.status_code, 302)
        self.assertEqual(user_update_profile_response.url, "/accounts/user-profile/")
        self.client.logout()

    def test_restaurant_can_view_profile_correctly(self):
        self.client.login(username="rest_user", password="123456test")
        restaurant_profile_response = self.client.get(
            "%s?action=View+Profile" % self.restaurant_profile_url
        )
        self.assertEqual(restaurant_profile_response.status_code, 200)
        self.assertTemplateUsed(
            restaurant_profile_response, "profile/restaurant_profile.html"
        )
        self.client.logout()

    def test_restaurant_can_edit_profile_correctly(self):
        self.client.login(username="rest_user", password="123456test")
        restaurant_profile_response = self.client.get(
            "%s?action=Edit+Profile" % self.restaurant_profile_url
        )
        self.assertEqual(restaurant_profile_response.status_code, 200)
        self.assertTemplateUsed(
            restaurant_profile_response, "profile/restaurant_profile.html"
        )

        # User edit profile content
        with open(self.image_file, "rb") as fp:
            upload_restaurant_form_data = {
                "submit-info": True,
                "username": "rest_user",
                "first_name": "Rest",
                "last_name": "User",
                "restaurant_name": "Restaurant Test Name",
                "photo": fp,
                "phone": "1234567890",
                "address": "6 Metrotech",
                "city": "Brooklyn",
                "zip_code": "11201",
                "state": "NY",
                "is_open": False,
            }
            restaurant_update_profile_response = self.client.post(
                self.restaurant_profile_url,
                upload_restaurant_form_data,
                HTTP_ACCEPT="application/json",
            )
        self.assertEqual(restaurant_update_profile_response.status_code, 302)
        self.assertEqual(
            restaurant_update_profile_response.url, "/accounts/restaurant-profile/"
        )
        self.client.logout()


class TestLogin(TestCase):
    def setUp(self):
        self.login_url = reverse("accessible_restaurant:login")
        self.client = Client()

        self.user = {
            "username": "normal_user",
            "password": "123456test",
        }

        User.objects.create_user(
            username="normal_user",
            email="test@test.com",
            password="123456test",
            is_user=True,
        )

        return super().setUp()

    def test_can_login_successfully(self):
        login_response = self.client.post(self.login_url, self.user, format="text/html")
        self.assertEqual(login_response.status_code, 302)
        self.assertEqual(login_response.url, "/")


class TestResetPassword(TestCase):
    def setUp(self):
        self.reset_url = reverse("accessible_restaurant:password-reset")
        self.client = Client()

        self.user = {
            "email": "test@test.com",
        }

        User.objects.create_user(
            username="normal_user",
            email="test@test.com",
            password="123456test",
            is_user=True,
        )

        return super().setUp()

    def test_can_login_successfully(self):
        reset_response = self.client.post(self.reset_url, self.user, format="text/html")
        self.assertEqual(reset_response.status_code, 302)
        self.assertEqual(reset_response.url, "/accounts/password-reset/done/")
