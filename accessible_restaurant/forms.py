from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from accessible_restaurant.models import (
    User,
    User_Profile,
    Restaurant_Profile,
    Review,
    ApprovalPendingUsers,
    ApprovalPendingRestaurants,
    Restaurant,
    Comment,
)
from django.utils.safestring import mark_safe


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

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
    def save(self, commit=True):
        user = super(UserSignUpForm, self).save(commit=False)
        user.is_user = True
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
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
            "auth_status",
        ]
        labels = {"zip_code": "Zip Code", "auth_status": "Authentication Status"}


class UserCertUpdateForm(forms.ModelForm):
    class Meta:
        model = ApprovalPendingUsers
        fields = [
            "auth_documents",
            "auth_status",
        ]
        labels = {
            "auth_documents": "Authentication Documents",
            "auth_status": "Authentication Status",
        }
        help_texts = {
            "auth_documents": ("Doctor's certificates and SSID allowed"),
        }


class UserCertVerifyForm(forms.ModelForm):
    class Meta:
        model = ApprovalPendingUsers
        fields = [
            "auth_status",
        ]
        labels = {"auth_status": "Authentication Status"}


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


class RestaurantCertUpdateForm(forms.ModelForm):
    class Meta:
        model = ApprovalPendingRestaurants
        restaurant = forms.ModelChoiceField(
            queryset=Restaurant.objects.filter(user=None), widget=forms.Select
        )
        fields = [
            "restaurant",
            "auth_documents",
        ]
        labels = {
            "restaurant": "Restaurant Choices",
            "auth_documents": "Authentication Documents",
        }
        help_texts = {
            "auth_documents": "Business Licenses Allowed",
        }

    def __init__(self, *args, **kwargs):
        super(RestaurantCertUpdateForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"].label_from_instance = self.label_from_instance
        self.fields["restaurant"].empty_label = "Select a restaurant"

    @staticmethod
    def label_from_instance(obj):
        return "%s, %s, %s" % (obj.name, obj.address, obj.city)


class RestaurantCertVerifyForm(forms.ModelForm):
    class Meta:
        model = ApprovalPendingRestaurants
        fields = [
            "auth_status",
        ]
        labels = {"auth_status": "Authentication Status"}


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
            # "images",
        ]
        widgets = {
            "rating": HorizontalRadioSelect(),
            "level_entry_rating": forms.RadioSelect,
            "wide_door_rating": forms.RadioSelect,
            "accessible_table_rating": forms.RadioSelect,
            "accessible_restroom_rating": forms.RadioSelect,
            "accessible_path_rating": forms.RadioSelect,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {
            "text": "New Comments",
        }
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "placeholder": "Write your comment here!",
                    "class": "form-control",
                    "rows": "5",
                }
            ),
        }


class ContactForm(forms.Form):
    Email = forms.EmailField(required=True)
    Subject = forms.CharField(required=True)
    Message = forms.CharField(widget=forms.Textarea, required=True)
