from django.test import TestCase
from django.urls import reverse, resolve
from django.test import SimpleTestCase
import accessible_restaurant
import django
from accessible_restaurant.views import (
    index_view,
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

# Create your tests here.


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("accessible_restaurant:index")
        # print(resolve(url))
        self.assertEquals(resolve(url).func, accessible_restaurant.views.index_view)

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
