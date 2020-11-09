from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser  # User
from PIL import Image


# Create your models here.


class User(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_restaurant = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


class User_Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="uprofile"
    )
    photo = models.ImageField(default="default.jpg", upload_to="user_profile_pics")
    phone = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, blank=True)
    zip_code = models.CharField(max_length=16, blank=True)
    state = models.CharField(max_length=32, blank=True)
    AUTH_STATUS_CHOICES = [
        ("certified", "Certified"),
        ("pending", "Pending"),
        ("uncertified", "Uncertified"),
    ]
    auth_status = models.CharField(
        max_length=16, choices=AUTH_STATUS_CHOICES, default="uncertified"
    )

    def __str__(self):
        return f"{self.user.username} User Profile"

    def save(self, *args, **kwargs):
        super(User_Profile, self).save(*args, **kwargs)

        img = Image.open(self.photo.path)
        img = img.convert("RGB")

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)


class ApprovalPendingUsers(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="auth"
    )
    auth_documents = models.FileField(blank=False, upload_to="documents/pdfs/")
    AUTH_STATUS_CHOICES = [
        ("approve", "Approve"),
        ("pending", "Pending"),
        ("disapprove", "Disapprove"),
    ]
    auth_status = models.CharField(
        max_length=16, choices=AUTH_STATUS_CHOICES, default="N/A"
    )
    time_created = models.DateTimeField(auto_now_add=True)


class Restaurant_Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="rprofile"
    )
    restaurant_name = models.CharField(max_length=50)
    photo = models.ImageField(
        default="default.jpg", upload_to="restaurant_profile_pics"
    )
    phone = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, blank=True)
    zip_code = models.CharField(max_length=16, blank=True)
    state = models.CharField(max_length=32, blank=True)
    is_open = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Restaurant Profile"

    def save(self, *args, **kwargs):
        super(Restaurant_Profile, self).save(*args, **kwargs)

        img = Image.open(self.photo.path)
        img = img.convert("RGB")

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)


class Restaurant(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="owner"
    )
    business_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=80)
    img_url = models.URLField(
        max_length=250,
        blank=True,
        default="https://i.pinimg.com/originals/4e/24/f5/4e24f523182e09376bfe8424d556610a.png",
    )
    rating = models.FloatField(blank=True, default=0)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default=0
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default=0
    )
    address = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, blank=True)
    zip_code = models.CharField(max_length=16, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    compliant = models.BooleanField(default=False)

    price = models.CharField(max_length=5, blank=True)
    category1 = models.CharField(max_length=128, blank=True)
    category2 = models.CharField(max_length=128, blank=True)
    category3 = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.name}"


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="review_user"
    )
    restaurant = models.ForeignKey(
        Restaurant, null=True, on_delete=models.CASCADE, related_name="relate_busid"
    )
    review_date = models.DateTimeField(default=datetime.now, editable=False)
    review_context = models.TextField()
    rating = models.PositiveIntegerField(blank=True, default=0)
    level_entry_rating = models.PositiveIntegerField(blank=True, default=0)
    wide_door_rating = models.PositiveIntegerField(blank=True, default=0)
    accessible_table_rating = models.PositiveIntegerField(blank=True, default=0)
    accessible_restroom_rating = models.PositiveIntegerField(blank=True, default=0)
    accessible_path_rating = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return f"{self.user} review on {self.restaurant}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, null=True, related_name="comments"
    )
    text = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["time"]

    def __str__(self):
        return "Comment {} by {} ".format(
            self.review.review_context, self.user.username
        )
