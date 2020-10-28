from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from accessible_restaurant.models import User, User_Profile, Restaurant_Profile


class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_user = True
        user.save()

        # TODO: create a user_profile for newly registered user

        return user


class RestaurantSignUpForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["username", "email", "password1", "password2"]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_restaurant = True
        user.save()

        # TODO: create a restaurant_profile for newly registered restaurant user

        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = [
            "photo",
            "phone",
            "address",
            "city",
            "zip_code",
            "state",
        ]
        labels = {
            "zip_code": "Zip Code",
        }


class RestaurantProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Restaurant_Profile
        fields = [
            "restaurant_name",
            "photo",
            "phone",
            "address",
            "city",
            "zip_code",
            "state",
            "is_open",
        ]
        labels = {
            "restaurant_name": "Restaurant Name",
            "zip_code": "Zip Code",
            "is_open": "Is Open",
        }
