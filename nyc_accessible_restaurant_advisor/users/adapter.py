from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from accessible_restaurant.forms import UserSignUpForm
from accessible_restaurant.models import User_Profile, User_Preferences
from django.conf import settings


class UserAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form=UserSignUpForm, commit=True):
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        """
        # Do not persist the user yet so we pass commit=False
        # (last argument)
        print("adapter is used!")
        user = super(UserAccountAdapter, self).save_user(
            request, user, form, commit=False
        )
        user.is_user = True
        User_Profile.objects.create(user=user)
        User_Preferences.objects.create(user=user)
        # user.save()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(CustomSocialAccountAdapter, self).save_user(
            request, sociallogin, form
        )
        # Do what ever you want with the user
        print("adapter is used!")
        user.is_user = True
        User_Profile.objects.create(user=user)
        User_Preferences.objects.create(user=user)
        user.save()
        return user
