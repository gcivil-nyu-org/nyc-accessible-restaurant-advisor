from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_restaurant = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='user_profile')
    phone = models.CharField(max_length=20)

class Restaurant_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='restaurant_profile')
    restaurant_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)


