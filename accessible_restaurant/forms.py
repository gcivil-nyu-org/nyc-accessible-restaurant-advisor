from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.db import transaction

from accessible_restaurant.models import (
    User,
    User_Profile,
    User_Preferences,
    Restaurant_Profile,
    Review,
    ApprovalPendingUsers,
    ApprovalPendingRestaurants,
    Restaurant,
    Comment,
    # Images,
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Username",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Username",
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


# class CustomAuthenticationForm(AuthenticationForm):
#     def confirm_login_allowed(self, user):
#         if not user.is_active or not user.is_validated:
#             raise forms.ValidationError('There was a problem with your login.', code='invalid_login')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "Username",
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
                "placeholder": "Email Address",
            }
        )


# class PickyAuthenticationForm(PasswordResetForm):
#     def confirm_login_allowed(self, user):
#         if not user.is_active:
#             raise forms.ValidationError("This account is inactive.",
#                 code='inactive',
#             )


class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MySetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "New Password",
            }
        )
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "form-control bg-white border-left-0 border-md",
                "placeholder": "New Password Confirmation",
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
            "borough",
            "city",
            "zip_code",
            "state",
            "auth_status",
        ]
        labels = {"zip_code": "Zip Code", "auth_status": "Authentication Status"}


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = User_Preferences

        fields = [
            "dining_pref1",
            "dining_pref2",
            "dining_pref3",
            "budget_pref",
            "location_pref",
            "dietary_pref",
            "cuisine_pref1",
            "cuisine_pref2",
        ]

        labels = {
            "dining_pref1": "When do you enjoy dining out? Select up to three options.",
            "dining_pref2": "",
            "dining_pref3": "",
            "budget_pref": "What is your preferred budget for dining out?",
            "location_pref": "Where do you prefer to dine out?",
            "dietary_pref": "Do you have any dietary preferences or restrictions?",
            "cuisine_pref1": "What cuisines do you enjoy? Select up to two options.",
            "cuisine_pref2": "",
        }


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
            "image1",
            "image2",
            "image3",
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


# class ImageForm(forms.ModelForm):
#     image = forms.ImageField(label='Image')
#     class Meta:
#         model = Images
#         fields = ('image', )


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
