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
        widgets = {
            'username': forms.TextInput(attrs={'class': 'username'}),
            'email': forms.TextInput(attrs={'class': 'email'}),
            'first_name': forms.TextInput(attrs={'class': 'first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'last_name'}),
            # 'password1': forms.PasswordInput(attrs={'class': 'password1'}),
            # 'password2': forms.PasswordInput(attrs={'class': 'password2'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'password'})

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
        widgets = {
            'username': forms.TextInput(attrs={'class': 'username'}),
            'email': forms.TextInput(attrs={'class': 'email'}),
            'password1': forms.PasswordInput(attrs={'class': 'password1'}),
            'password2': forms.PasswordInput(attrs={'class': 'password2'}),
        }

    def __init__(self, *args, **kwargs):
        super(RestaurantSignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'password'})

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_restaurant = True
        user.save()

        # TODO: create a restaurant_profile for newly registered restaurant user

        return user