from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accessible_restaurant"
urlpatterns = [
    path("home/", views.index_view, name="index"),
    path(
        "accounts/login",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "accounts/logout",
        auth_views.LogoutView.as_view(template_name="index.html"),
        name="logout",
    ),
    path("accounts/signup/", views.signup_view, name="signup"),
    path(
        "accounts/signup/usersignup/",
        views.UserSignUpView.as_view(),
        name="user_signup",
    ),
    path(
        "accounts/signup/restaurantsignup/",
        views.RestaurantSignUpView.as_view(),
        name="restaurant_signup",
    ),
    path("accounts/signup/emailsent/", views.emailsent_view, name="emailsent"),
    path("accounts/<uidb64>/<token>", views.activate_account, name="activate"),
    # Profile urls
    path("accounts/user-profile/", views.user_profile_view, name="user_profile"),
    path(
        "accounts/restaurant-profile/",
        views.restaurant_profile_view,
        name="restaurant_profile",
    ),
    # Browse restaurant
    path("restaurants/browse/<int:page>/<sort_property>", views.restaurant_list_view, name="browse"),
    path(
        "restaurants/detail/<business_id>", views.restaurant_detail_view, name="detail"
    ),

]
