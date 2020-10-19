from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

app_name='accessible_restaurant'
urlpatterns = [
    # path('accounts/login', views.login_view, name='login'),
    path('accounts/home', views.home, name="home"),
    path('accounts/login', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/profile', views.profile, name='profile'),
    path('accounts/logout', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/signup/usersignup/', views.UserSignUpView.as_view(), name='user_signup'),
    path('accounts/signup/restaurantsignup/', views.RestaurantSignUpView.as_view(), name='restaurant_signup'),
    path('accounts/signup/emailsent/', views.emailsent_view, name='emailsent'),
    path('accounts/<uidb64>/<token>', views.activate_account, name="activate"), 
]