from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from accessible_restaurant.models import User, User_Profile, Restaurant_Profile, Review
from django.utils.safestring import mark_safe


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


# User update form
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
            "auth_documents",
        ]
        labels = {"zip_code": "Zip Code", "auth_documents": "Authorization Documents"}


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


class HorizontalRadioSelect(forms.RadioSelect):
    template_name = "horizontal_select.html"


class ReviewPostForm(forms.ModelForm):
    SCORE_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    rating = forms.ChoiceField(label=("General Rating"), choices=SCORE_CHOICES)
    level_entry_rating = forms.ChoiceField(
        label=("Level Entry Rating"), choices=SCORE_CHOICES
    )
    wide_door_rating = forms.ChoiceField(
        label=("Wide Door Rating"), choices=SCORE_CHOICES
    )
    accessible_table_rating = forms.ChoiceField(
        label=("Accessible Table Rating"), choices=SCORE_CHOICES
    )
    accessible_restroom_rating = forms.ChoiceField(
        label=("Accessible Restroom Rating"), choices=SCORE_CHOICES
    )
    accessible_path_rating = forms.ChoiceField(
        label=("Accessible Path Rating"), choices=SCORE_CHOICES
    )

    class Meta:
        model = Review
        fields = [
            "rating",
            "level_entry_rating",
            "wide_door_rating",
            "accessible_table_rating",
            "accessible_restroom_rating",
            "accessible_path_rating",
            "review_context",
        ]
        widgets = {
            "rating": HorizontalRadioSelect(),
            "level_entry_rating": forms.RadioSelect,
            "wide_door_rating": forms.RadioSelect,
            "accessible_table_rating": forms.RadioSelect,
            "accessible_restroom_rating": forms.RadioSelect,
            "accessible_path_rating": forms.RadioSelect,
        }
