from django.urls import include, path
from . import views

app_name='accessible_restaurant'
urlpatterns = [
    path('home/', views.index_view, name='index'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/signup/usersignup/', views.UserSignUpView.as_view(), name='user_signup'),
    path('accounts/signup/restaurantsignup/', views.RestaurantSignUpView.as_view(), name='restaurant_signup'),
    path('accounts/signup/emailsent/', views.emailsent_view, name='emailsent'),
    path('accounts/<uidb64>/<token>', views.activate_account, name="activate"),
    path('profile/userprofile', views.userprofile_view, name='user_profile'),
    path('profile/restaurantprofile', views.restaurantprofile_view, name='restaurant_profile'),
]