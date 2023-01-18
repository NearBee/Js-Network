import pytz
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import new_post_form
from .models import New_Post, User


def index(request):
    return render(request, "network/index.html", {"posts": New_Post.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    timezones = pytz.common_timezones
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        timezone = request.POST["timezone"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "network/register.html",
                {"message": "Passwords must match.", "timezones": timezones},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)  # type: ignore
            tz = pytz.timezone(timezone)
            user.timezone = tz
            user.save()
        except IntegrityError as ie:
            return render(
                request,
                "network/register.html",
                {"message": "Username already taken.", "timezones": timezones},
            )

        except ValueError as ve:
            return render(
                request,
                "network/register.html",
                {"message": "No information was entered", "timezones": timezones},
            )

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html", {"timezones": timezones})


@login_required(redirect_field_name="", login_url="login")
def new_post(request):
    if request.method == "POST":
        post_forms = new_post_form(request.POST)
        if post_forms.is_valid():
            finished_post_forms = post_forms.save(commit=False)
            finished_post_forms.user = request.user
            finished_post_forms.save()
            post_forms = new_post_form()
            return redirect("index")
    return render(request, "network/newpost.html", {"new_post_form": new_post_form})
