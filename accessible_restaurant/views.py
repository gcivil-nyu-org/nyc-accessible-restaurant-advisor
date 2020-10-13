from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
# from django.contrib import messages
from django.views.generic import CreateView
from django.core.mail import send_mail


from .forms import UserSignUpForm, RestaurantSignUpForm
from .models import User


# Create your views here.


def login_view(request):
    return render(request, 'accounts/login.html')


def signup_view(request):
    return render(request, 'accounts/register.html')


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'accounts/userRegister.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accessible_restaurant:login')


class RestaurantSignUpView(CreateView):
    model = User
    form_class = RestaurantSignUpForm
    template_name = 'accounts/restaurantRegister.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'restaurant'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        restaurant = form.save()
        login(self.request, restaurant)
        return redirect('accessible_restaurant:login')
