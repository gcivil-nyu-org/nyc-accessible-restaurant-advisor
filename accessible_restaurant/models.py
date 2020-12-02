from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
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

    def validate_phone(value):
        if len(str(value)) != 10:
            raise ValidationError(
                _("%(value)s must be 10 digits."),
                params={"value": value},
            )

    phone = models.PositiveSmallIntegerField(
        blank=True, validators=[validate_phone], default=0000000000
    )  # Updated

    address = models.CharField(max_length=128, blank=True)

    BOROUGH_CHOICES = [
        ("Manhattan", "Manhattan"),
        ("Brooklyn", "Brooklyn"),
        ("Queens", "Queens"),
        ("The Bronx", "The Bronx"),
        ("Staten Island", "Staten Island"),
        ("Not Applicable", "Not Applicable"),
    ]
    borough = models.CharField(
        max_length=128, choices=BOROUGH_CHOICES, default="None Selected"
    )
    city = models.CharField(max_length=64, blank=True)  # choices

    def validate_zip(value):
        if len(str(value)) != 5:
            raise ValidationError(
                _("%(value)s must be 5 digits."),
                params={"value": value},
            )

    zip_code = models.PositiveSmallIntegerField(
        blank=True, validators=[validate_zip], default=00000
    )  # Updated

    STATE_CHOICES = [
        ("Alabama", "Alabama"),
        ("Alaska", "Alaska"),
        ("Arizona", "Arizona"),
        ("Arkansas", "Arkansas"),
        ("California", "California"),
        ("Colorado", "Colorado"),
        ("Connecticut", "Connecticut"),
        ("Delaware", "Delaware"),
        ("District of Columbia", "District of Columbia"),
        ("Florida", "Florida"),
        ("Georgia", "Georgia"),
        ("Hawaii", "Hawaii"),
        ("Idaho", "Idaho"),
        ("Illinois", "Illinois"),
        ("Indiana", "Indiana"),
        ("Iowa", "Iowa"),
        ("Kansas", "Kansas"),
        ("Kentucky", "Kentucky"),
        ("Louisiana", "Louisiana"),
        ("Maine", "Maine"),
        ("Montana", "Montana"),
        ("Nebraska", "Nebraska"),
        ("Nevada", "Nevada"),
        ("New Hampshire", "New Hampshire"),
        ("New Jersey", "New Jersey"),
        ("New Mexico", "New Mexico"),
        ("New York", "New York"),
        ("North Carolina", "North Carolina"),
        ("North Dakota", "North Dakota"),
        ("Ohio", "Ohio"),
        ("Oklahoma", "Oklahoma"),
        ("Oregon", "Oregon"),
        ("Maryland", "Maryland"),
        ("Massachusetts", "Massachusetts"),
        ("Michigan", "Michigan"),
        ("Minnesota", "Minnesota"),
        ("Mississippi", "Mississippi"),
        ("Missouri", "Missouri"),
        ("Pennsylvania", "Pennsylvania"),
        ("Rhode Island", "Rhode Island"),
        ("South Carolina", "South Carolina"),
        ("South Dakota", "South Dakota"),
        ("Tennessee", "Tennessee"),
        ("Texas", "Texas"),
        ("Utah", "Utah"),
        ("Vermont", "Vermont"),
        ("Virginia", "Virginia"),
        ("Washington", "Washington"),
        ("West Virginia", "West Virginia"),
        ("Wisconsin", "Wisconsin"),
        ("Wyoming", "Wyoming"),
    ]
    state = models.CharField(
        max_length=128, choices=STATE_CHOICES, default="None Selected"
    )  # choices
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


class User_Preferences(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="upreferences"
    )
    DINING = [
        ("Breakfast", "Breakfast"),
        ("Lunch", "Lunch"),
        ("Dinner", "Dinner"),
        ("Non-Alcoholic Drinks", "Non-Alcoholic Drinks"),
        ("Alcoholic Drinks", "Alcoholic Drinks"),
        ("Dessert", "Dessert"),
        ("No Preference", "No Preference"),
    ]
    dining_pref1 = models.CharField(
        max_length=20, choices=DINING, default="No Preference"
    )
    dining_pref2 = models.CharField(
        max_length=20, choices=DINING, default="No Preference"
    )
    dining_pref3 = models.CharField(
        max_length=20, choices=DINING, default="No Preference"
    )

    BUDGET = [
        ("$", "$"),
        ("$$", "$$"),
        ("$$$", "$$$"),
        ("$$$$", "$$$$"),
        ("No Preference", "No Preference"),
    ]
    budget_pref = models.CharField(
        max_length=15, choices=BUDGET, default="No Preference"
    )

    LOCATION = [
        ("Near Home", "Near Home"),
        ("Within My Borough", "Within My Borough"),
        ("Outside My Borough", "Outside My Borough"),
        ("No Preference", "No Preference"),
    ]
    location_pref = models.CharField(
        max_length=20, choices=LOCATION, default="No Preference"
    )

    DIETARY = [
        ("Vegetarian", "Vegetarian"),
        ("Gluten-Free", "Gluten-Free"),
        ("Salads Available", "Salads Available"),
        ("None", "None"),
    ]
    dietary_pref = models.CharField(max_length=20, choices=DIETARY, default="None")

    CUISINE = [
        ("Asian", "Asian"),
        ("American", "American"),
        ("Caribbean", "Caribbean"),
        ("European", "European"),
        ("Indian", "Indian"),
        ("Latin American", "Latin American"),
        ("Mediterranean", "Mediterranean"),
        ("Middle Eastern", "Middle Eastern"),
        ("Southern", "Southern"),
        ("No Preference", "No Preference"),
    ]
    cuisine_pref1 = models.CharField(
        max_length=16, choices=CUISINE, default="No Preference"
    )
    cuisine_pref2 = models.CharField(
        max_length=16, choices=CUISINE, default="No Preference"
    )

    def __str__(self):
        return f"{self.user.username} User Preferences"

    # for later: add restaurants from User's favorite list

    # def save(self, *args, **kwargs):
    #     super(User_Profile, self).save(*args, **kwargs)
    #
    #     img = Image.open(self.photo.path)
    #     img = img.convert("RGB")
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.photo.path)


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

    # def save(self, *args, **kwargs):
    #     super(Restaurant_Profile, self).save(*args, **kwargs)
    #
    #     img = Image.open(self.photo.path)
    #     img = img.convert("RGB")
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.photo.path)


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
    review_count = models.FloatField(blank=True, default=0)
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
    main_category1 = models.CharField(max_length=128, blank=True)
    main_category2 = models.CharField(max_length=128, blank=True)
    main_category3 = models.CharField(max_length=128, blank=True)
    cuisine = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.name}"


class ApprovalPendingRestaurants(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="auth_user"
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, null=True, related_name="auth_rest"
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


class FAQ(models.Model):
    question = models.CharField(max_length=128)
    answer = models.TextField()


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite")
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="favorite"
    )

    def __str__(self):
        return f"{self.user} likes {self.restaurant}"
