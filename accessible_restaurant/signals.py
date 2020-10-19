from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, User_Profile, Restaurant_Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        if user.is_user:
            User_Profile.objects.create(user=user)

        elif user.is_restaurant:
            Restaurant_Profile.objects.create(user=user)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    user = instance
    if user.is_user:
        instance.user_profile.save()

    elif user.is_restaurant:
        instance.restaurant_profile.save()