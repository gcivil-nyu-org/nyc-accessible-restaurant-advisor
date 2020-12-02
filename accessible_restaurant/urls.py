from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm, MyPasswordResetForm

app_name = "accessible_restaurant"
urlpatterns = [
    path("", views.index_view_personalized, name="index"),
    path("about/", views.about_view, name="about"),
    path(
        "accounts/login",
        auth_views.LoginView.as_view(
            template_name="accounts/signin.html",
            authentication_form=UserLoginForm,
        ),
        name="login",
    ),
    path(
        "accounts/logout",
        auth_views.LogoutView.as_view(template_name="index.html"),
        name="logout",
    ),
    path(
        "accounts/password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/passwordReset.html",
            form_class=MyPasswordResetForm,
        ),
        name="password-reset",
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
    # <sort_property>/
    path(
        "restaurants/browse/<page>/",
        views.restaurant_list_view,
        name="browse",
    ),
    path(
        "restaurants/detail/<business_id>", views.restaurant_detail_view, name="detail"
    ),
    # Review and comments
    path("writeareview/<business_id>", views.write_review_view, name="write_review"),
    path(
        "restaurants/detail/<business_id>/<review_id>/",
        views.add_comment_view,
        name="add_comment",
    ),
    path("user_detail/<user>", views.user_detail_view, name="public_facing"),
    # admin manage the certificate
    path("manage/", views.authentication_view, name="authenticate"),
    # Frequently Asked Questions
    path("faq/", views.faq_view, name="faq"),
]
