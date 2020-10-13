from django.urls import include, path
from . import views

app_name='accessible_restaurant'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/login', views.login_view(), name='login'),
    path('accounts/signup/', views.signup_view(), name='signup'),
    path('accounts/signup/usersignup/', views.UserSignUpView.as_view(), name='user_signup'),
    path('accounts/signup/restaurantsignup/', views.RestaurantSignUpView.as_view(), name='restaurant_signup'),
]