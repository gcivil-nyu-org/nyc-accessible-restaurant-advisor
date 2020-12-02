from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Username"
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Email Address",
            }
        )
        self.fields["first_name"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "First Name",
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Last Name",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "PasswordConfirmation",
            }
        )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Username"
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Email Address",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "PasswordConfirmation",
            }
        )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_restaurant = True
        user.save()

        # TODO: create a restaurant_profile for newly registered restaurant user

        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Username"
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Password",
            }
        )


class MyPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Email Address"
            }
        )


class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MySetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "New Password"
            }
        )
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "New Password Confirmation"
            }
        )


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
    # SCORE_CHOICES = (
    #     (1, '☆'),
    #     (2, '☆'),
    #     (3, '☆'),
    #     (4, '☆'),
    #     (5, '☆'),
    # )
    # rating = forms.ChoiceField(label="General Rating", choices=SCORE_CHOICES)
    # level_entry_rating = forms.ChoiceField(
    #     label="Level Entry Rating", choices=SCORE_CHOICES
    # )
    # wide_door_rating = forms.ChoiceField(
    #     label="Wide Door Rating", choices=SCORE_CHOICES
    # )
    # accessible_table_rating = forms.ChoiceField(
    #     label="Accessible Table Rating", choices=SCORE_CHOICES
    # )
    # accessible_restroom_rating = forms.ChoiceField(
    #     label="Accessible Restroom Rating", choices=SCORE_CHOICES
    # )
    # accessible_path_rating = forms.ChoiceField(
    #     label="Accessible Path Rating", choices=SCORE_CHOICES
    # )
    #
    # class Meta:
    #     model = Review
    #     fields = [
    #         "rating",
    #         "level_entry_rating",
    #         "wide_door_rating",
    #         "accessible_table_rating",
    #         "accessible_restroom_rating",
    #         "accessible_path_rating",
    #         "review_context",
    #     ]
    #     widgets = {
    #         "rating": HorizontalRadioSelect(),
    #         "level_entry_rating": forms.RadioSelect,
    #         "wide_door_rating": forms.RadioSelect,
    #         "accessible_table_rating": forms.RadioSelect,
    #         "accessible_restroom_rating": forms.RadioSelect,
    #         "accessible_path_rating": forms.RadioSelect,
    #     }

    SCORE_CHOICES = (
        (5, "☆"),
        (4, "☆"),
        (3, "☆"),
        (2, "☆"),
        (1, "☆"),
    )
    rating = forms.ChoiceField(
        label="General Rating", widget=forms.RadioSelect, choices=SCORE_CHOICES
    )
    level_entry_rating = forms.ChoiceField(
        label="Level Entry Rating", widget=forms.RadioSelect, choices=SCORE_CHOICES
    )
    wide_door_rating = forms.ChoiceField(
        label="Wide Door Rating", widget=forms.RadioSelect, choices=SCORE_CHOICES
    )
    accessible_table_rating = forms.ChoiceField(
        label="Accessible Table Rating", widget=forms.RadioSelect, choices=SCORE_CHOICES
    )
    accessible_restroom_rating = forms.ChoiceField(
        label="Accessible Restroom Rating",
        widget=forms.RadioSelect,
        choices=SCORE_CHOICES,
    )
    accessible_path_rating = forms.ChoiceField(
        label="Accessible Path Rating", widget=forms.RadioSelect, choices=SCORE_CHOICES
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
        labels = {
            "review_context": "Review",
        }
        widgets = {
            "review_context": forms.Textarea(
                attrs={
                    "placeholder": "Write your review here!",
                    "rows": "17",
                    "style": "resize:none;",
                }
            )
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
                    "style": "resize:none;",
                }
            ),
        }


class ContactForm(forms.Form):
    Email = forms.EmailField(required=True)
    Subject = forms.CharField(required=True)
    Message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Write your question or suggestions here!",
                "class": "form-control",
                "rows": "10",
                "style": "resize:none;",
            }
        ),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["Email"].widget.attrs.update({"class": "form-control"})
        self.fields["Subject"].widget.attrs.update({"class": "form-control"})
