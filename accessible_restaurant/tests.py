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


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse("accessible_restaurant:index")
        self.logout_url = reverse("accessible_restaurant:logout")
        self.signup_url = reverse("accessible_restaurant:signup")
        self.emailsent_url = reverse("accessible_restaurant:emailsent")
        self.activate_url = reverse(
            "accessible_restaurant:activate", args=["uid", "token"]
        )
        self.userprofile_url = reverse("accessible_restaurant:user_profile")
        self.resprofile_url = reverse("accessible_restaurant:restaurant_profile")
        self.browse_url = reverse("accessible_restaurant:browse", args=[10])
        self.detail_url = reverse(
            "accessible_restaurant:detail", args=["FaPtColHYcTnZAxtoM33cA"]
        )

        self.usertest = User.objects.create(
            username="huanjin", first_name="Huanjin", last_name="Zhang"
        )

    def test_index_view_GET(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_logout_view_GET(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_signup_view_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_email_sent_view_GET(self):
        response = self.client.get(self.emailsent_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/emailSent.html")

    # def test_activate_view_GET(self):
    #     User.objects.create(
    #         username="username",
    #         first_name="first",
    #         last_name="last"
    #     )
    #     response = self.client.get(self.activate_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "accountss/activate_account.html")

    def test_browse_view_GET(self):
        response = self.client.get(self.browse_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/browse.html")

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
        self.assertTemplateUsed(response, "restaurants/detail.html")

    def test_user_profile_view_POST(self):
        self.client.login(username="huanjin", password="test123456")
        User_Profile.objects.create(
            photo="default.jpg",
            phone="3474223609",
            address="35 River Drive South",
            city="Jersey City",
            zip_code="07310",
            state="NJ",
        )
        response = self.client.post(self.userprofile_url)
        self.assertEqual(response.status_code, 302)

    def test_res_profile_view_POST(self):
        self.client.login(username="huanjin", password="test123456")
        Restaurant_Profile.objects.create(
            restaurant_name="name",
            photo="default.jpg",
            phone="3474223609",
            address="35 River Drive South",
            city="Jersey City",
            zip_code="07310",
            state="NJ",
            is_open=True,
        )
        response = self.client.post(self.resprofile_url)
        self.assertEqual(response.status_code, 302)
