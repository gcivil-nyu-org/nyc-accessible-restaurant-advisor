from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
# from django.contrib import messages
from django.views.generic import CreateView


from .forms import UserSignUpForm, RestaurantSignUpForm
from .models import User


# Create your views here.


def signup_view(request):
    return render(request, 'registration/register.html')


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'registration/userRegister.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accessible_restaurant: login')


class RestaurantSignUpView(CreateView):
    model = User
    form_class = RestaurantSignUpForm
    template_name = 'registration/restaurantRegister.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'restaurant'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        restaurant = form.save()
        login(self.request, restaurant)
        return redirect('accessible_restaurant: login')

# [Only for Backup Purpose] Views as Function

# def login_view(request):
#     return render(request, 'login.html')
#
# def signup_view(request):
#     pass
#
# def user_signup_view(request):
#     if request.method == 'POST':
#         form = UserSignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_user = True
#             user.is_restaurant = False
#             user.save()
#             form.save_m2m()
#             username = form.cleaned_data.get('username')
#             messages.success(request, 'User account was created for ' + username)
#             login(self.request, user)
#             return redirect('login')
#     else:
#         form = UserSignUpForm()
#     context = {'form', form}
#     return render(request, 'registration/userRegister.html', context)
#
#
# def restaurant_signup_view(request):
#     if request.method == 'POST':
#         form = RestaurantSignUpForm(request.POST)
#         if form.is_valid():
#             restaurant = form.save(commit=False)
#             restaurant.is_user = False
#             restaurant.is_restaurant = True
#             restaurant.save()
#             form.save_m2m()
#             username = form.cleaned_data.get('username')
#             messages.success(request, 'User account was created for ' + username)
#             return redirect('login')
#     else:
#         form = RestaurantSignUpForm()
#     context = {'form', form}
#     return render(request, 'registration/restaurantRegister.html', context)