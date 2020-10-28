from django.test import TestCase, Client
from django.urls import reverse
from accessible_restaurant.models import (
    User,
    User_Profile,
    Restaurant_Profile,
    Restaurant,
)
import json

# Create your tests here.


# Test views.py
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse("accessible_restaurant:index")
        self.logout_url = reverse("accessible_restaurant:logout")
        self.signup_url = reverse("accessible_restaurant:signup")
        self.emailsent_url = reverse("accessible_restaurant:emailsent")
        self.activate_url = reverse("accessible_restaurant:activate", args=["uid","token"])
        self.userprofile_url = reverse("accessible_restaurant:user_profile")
        self.resprofile_url = reverse("accessible_restaurant:restaurant_profile")
        self.browse_url = reverse("accessible_restaurant:browse", args=["page"])
        self.detail_url = reverse("accessible_restaurant:detail", args=["business_id"])

        self.usersignup_url = reverse("accessible_restaurant:user_signup")
        self.restaurantsignup_url = reverse("accessible_restaurant:restaurant_signup")

        self.user_test = User.objects.create(
            username="username",
            email="testemail@gmail.com",
            first_name="first",
            last_name="last",
            password1="password123",
            password2="password123",
        )
        self.resuser_test = User.objects.create(
            username="username",
            email="testemail@gmail.com",
            password1="password123",
            password2="password123",
        )

        return super().setUp()

    def test_index_view_GET(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_logout_view_GET(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/logout.html")

    def test_signup_view_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_email_sent_view_GET(self):
        response = self.client.get(self.emailsent_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/emailSent.html")

    #    def test_activate_view_GET(self):
    #        response = self.client.get(self.activate_url)

    def test_browse_view_GET(self):
        response = self.client.get(self.browse_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/browse.html")

    def test_detail_view_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/detail.html")

    # copy from previous code
    def test_can_view_page_correctly(self):
        response = self.client.get(self.usersignup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/userRegister.html")

    def test_can_register_user(self):
        response = self.client.post(
            self.usersignup_url, self.user_test, format="text/html"
        )
        self.assertEqual(response.status_code, 200)

    def test_can_view_page_correctly(self):
        response = self.client.get(self.restaurantsignup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/restaurantRegister.html")

    def test_can_register_user(self):
        response = self.client.post(
            self.restaurantsignup_url,
            self.resuser_test,
            format="text/html",
            follow=True,
        )
        self.assertEqual(response.status_code, 200)


class UserSignUpTest(TestCase):
    def setUp(self):
        self.usersignup_url = reverse("accessible_restaurant:user_signup")
        self.user = {
            "username": "username",
            "email": "testemail@gmail.com",
            "first_name": "first",
            "last_name": "last",
            "password1": "password123",
            "password2": "password123",
        }
        return super().setUp()

    def test_can_view_page_correctly(self):
        response = self.client.get(self.usersignup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/userRegister.html")

    def test_can_register_user(self):
        response = self.client.post(self.usersignup_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 200)


class RestaurantSignUpTest(TestCase):
    def setUp(self):
        self.restaurantsignup_url = reverse("accessible_restaurant:restaurant_signup")
        self.restaurant = {
            "username": "username",
            "email": "testemail@gmail.com",
            "password1": "password123",
            "password2": "password123",
        }
        return super().setUp()

    def test_can_view_page_correctly(self):
        response = self.client.get(self.restaurantsignup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/restaurantRegister.html")

    def test_can_register_user(self):
        response = self.client.post(
            self.restaurantsignup_url, self.restaurant, format="text/html", follow=True
        )
        self.assertEqual(response.status_code, 200)
