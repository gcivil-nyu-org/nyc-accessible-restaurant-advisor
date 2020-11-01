from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

# from django.contrib import messages
from django.views.generic import CreateView
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# from .token_generator import generate_token
from django.core.mail import EmailMessage

from .forms import (
    UserSignUpForm,
    RestaurantSignUpForm,
    UserUpdateForm,
    UserProfileUpdateForm,
    RestaurantProfileUpdateForm,
)
from django.contrib.auth.decorators import login_required

from .models import User, Restaurant
from .utils import get_restaurant_list, get_restaurant, get_page_range, get_star_list


# Create your views here.
def index_view(request):
    return render(request, "index.html")


def logout_view(request):
    return render(request, "accounts/logout.html")


def signup_view(request):
    if request.method == "GET":
        return render(request, "accounts/register.html")


def emailsent_view(request):
    if request.method == "GET":
        return render(request, "accounts/emailSent.html")


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
        return render(request, "accounts/activate_confirmation.html")
    return render(request, "accounts/signup.html")


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = "accounts/userRegister.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "user"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # check if user's email has already exist in the database
        user_email = form.cleaned_data.get("email")
        if User.objects.filter(email=user_email).exists():
            return render(
                self.request,
                self.template_name,
                {
                    "error_message": "Email has already been registered.",
                    "form": form,
                },
            )
        user = form.save()
        user.is_active = False
        user.save()
        # Email verification
        current_site = get_current_site(self.request)
        email_subject = "Activate Your NYC Accessible Restaurant Advisor Account!"
        message = render_to_string(
            "accounts/activate_account.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": PasswordResetTokenGenerator().make_token(user),
            },
        )
        to_email = form.cleaned_data.get("email")
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        return redirect("accessible_restaurant:emailsent")


class RestaurantSignUpView(CreateView):
    model = User
    form_class = RestaurantSignUpForm
    template_name = "accounts/restaurantRegister.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "restaurant"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # check if restaurant's email has already exist in the database
        restaurant_email = form.cleaned_data.get("email")
        if User.objects.filter(email=restaurant_email).exists():
            return render(
                self.request,
                self.template_name,
                {
                    "error_message": "Email has already been registered.",
                    "form": form,
                },
            )
        restaurant = form.save()
        restaurant.is_active = False
        restaurant.save()
        # Email verification
        current_site = get_current_site(self.request)
        email_subject = "Activate Your NYC Accessible Restaurant Advisor Account!"
        message = render_to_string(
            "accounts/activate_account.html",
            {
                "user": restaurant,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(restaurant.pk)),
                "token": PasswordResetTokenGenerator().make_token(restaurant),
            },
        )
        to_email = form.cleaned_data.get("email")
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        return redirect("accessible_restaurant:emailsent")


@login_required
def user_profile_view(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.uprofile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            print("profile form successfully saved!")
            messages.success(request, f'{"Your profile has been updated!"}')
            return redirect("accessible_restaurant:user_profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.uprofile)

    context = {"user_form": u_form, "profile_form": p_form}
    return render(request, "profile/user_profile.html", context)


@login_required
def restaurant_profile_view(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = RestaurantProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.rprofile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'{"Your profile has been updated!"}')
            return redirect("accessible_restaurant:restaurant_profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = RestaurantProfileUpdateForm(instance=request.user.rprofile)

    context = {
        "user_form": u_form,
        "profile_form": p_form,
    }
    return render(request, "profile/restaurant_profile.html", context)


def restaurant_list_view(request, page, sort_property):
    client_ip = get_client_ip(request)
    restaurant_list = get_restaurant_list(page, 10, sort_property, client_ip)
    star_list = get_star_list()
    for restaurant in restaurant_list:
        full, half, null = star_list[restaurant["rating"]]
        restaurant["full"] = full
        restaurant["half"] = half
        restaurant["null"] = null

    # Page count
    total_restaurant = Restaurant.objects.count()
    total_page = total_restaurant // 10
    if total_restaurant % 10 == 0:
        total_page -= 1

    # Previous and next page numbers
    page_range = get_page_range(int(total_page), page + 1)
    page_exceed_error = (
        "page number exceeds maximum page number, please choose valid page"
    )
    context = {
        "restaurants": restaurant_list,
        "star_list": star_list,
        "page_num": page,
        "total_page": total_page,
        "page_range": page_range,
        "page_exceed_error": page_exceed_error,
        "sort_property": sort_property,
    }
    return render(request, "restaurants/browse.html", context)


def restaurant_detail_view(request, business_id):
    try:
        restaurant = Restaurant.objects.get(business_id=business_id)
    except (KeyError, Restaurant.DoesNotExist):
        return render(
            request,
            "restaurants/error.html",
            {
                "business_id": business_id,
                "error_message": "Restaurant not found!",
            },
        )
    else:
        response = get_restaurant(restaurant.business_id)
        star_list = get_star_list()
        full, half, null = star_list[restaurant.rating]

        restaurant_data = response["restaurant_data"]
        restaurant_reviews = response["restaurant_reviews"]

        # Rating stars
        for review in restaurant_reviews["reviews"]:
            r_full, r_half, r_null = star_list[float(review["rating"])]
            review["full"] = r_full
            review["half"] = r_half
            review["null"] = r_null

        # Get open hours and is_open status
        hours = []
        is_open_now = False
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        if restaurant_data["hours"]:
            is_open_now = restaurant_data["hours"][0]["is_open_now"]
            for day in restaurant_data["hours"][0]["open"]:
                index = int(day["day"])
                day["weekday"] = weekdays[index]
                start = day["start"]
                end = day["end"]
                day["start"] = start[:2] + ":" + start[2:]
                day["end"] = end[:2] + ":" + end[2:]
                hours.append(day)

        context = {
            "restaurant": restaurant,
            "restaurant_data": restaurant_data,
            "restaurant_review": restaurant_reviews,
            "full": full,
            "half": half,
            "null": null,
            "hours": hours,
            "is_open_now": is_open_now,
        }
        return render(request, "restaurants/detail.html", context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
