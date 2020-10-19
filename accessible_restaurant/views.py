from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
# from django.contrib import messages
from django.views.generic import CreateView

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from .token_generator import generate_token
from django.core.mail import EmailMessage


from .forms import UserSignUpForm, RestaurantSignUpForm, UserUpdateForm, UserProfileUpdateForm, RestaurantProfileUpdateForm
from .models import User


# Create your views here.


def login_view(request):
    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/register.html')


def emailsent_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/emailSent.html')


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user.username)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/activate_confirmation.html')
    return render(request, 'accounts/signup.html')


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'accounts/userRegister.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # check if user's email has already exist in the database
        user_email = form.cleaned_data.get('email')
        if User.objects.filter(email=user_email).exists():
            return render(self.request, self.template_name, {
                'error_message': "Email has already been registered.",
                'form': form,
            })
        user = form.save()
        user.is_active = False
        user.save()
        # Email verification
        current_site = get_current_site(self.request)
        email_subject = "Activate Your NYC Accessible Restaurant Advisor Account!"
        message = render_to_string('accounts/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': PasswordResetTokenGenerator().make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        return redirect('accessible_restaurant:emailsent')


class RestaurantSignUpView(CreateView):
    model = User
    form_class = RestaurantSignUpForm
    template_name = 'accounts/restaurantRegister.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'restaurant'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # check if restaurant's email has already exist in the database
        restaurant_email = form.cleaned_data.get('email')
        if User.objects.filter(email=restaurant_email).exists():
            return render(self.request, self.template_name, {
                'error_message': "Email has already been registered.",
                'form': form,
            })
        restaurant = form.save()
        restaurant.is_active = False
        restaurant.save()
        # Email verification
        current_site = get_current_site(self.request)
        email_subject = "Activate Your NYC Accessible Restaurant Advisor Account!"
        message = render_to_string('accounts/activate_account.html', {
            'user': restaurant,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(restaurant.pk)),
            'token': PasswordResetTokenGenerator().make_token(restaurant),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        return redirect('accessible_restaurant:emailsent')

@login_required
def user_profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST,
                                       request.FILES,
                                       instance=request.user.user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('user_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user)

    context = {
        'user_form': u_form,
        'profile_form': p_form
    }
    return render(request, 'accounts/user_profile.html', context)


@login_required
def restaurant_profile_view(request):
    if request.method == 'POST':
        user = request.user
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = RestaurantProfileUpdateForm(request.POST,
                                             request.FILES,
                                             instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('restaurant_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = RestaurantProfileUpdateForm(instance=request.user)

    context = {
        'user_form': u_form,
        'profile_form': p_form,
    }
    return render(request, 'accounts/restaurant_profile.html', context)




