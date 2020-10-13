from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from accessible_restaurant.models import User, User_Profile, Restaurant_Profile

class UserSignUpForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
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
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_restaurant = True
        user.save()

        # TODO: create a restaurant_profile for newly registered restaurant user

        return user