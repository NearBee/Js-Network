import pytz
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import new_post_form
from .models import New_Post, User


def index(request):
    posts = New_Post.objects.all()
    paginated = Paginator(posts, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginated.get_page(page_number)

    return render(
        request,
        "network/index.html",
        {"posts": page_obj},
    )


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


@login_required(redirect_field_name="", login_url="login")
def profile_view(request, username):
    target_user = User.objects.get(username=username)
    posts = request.user.post.all()
    paginated = Paginator(posts, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginated.get_page(page_number)
    if request.user != username:
        new_posts = New_Post.objects.filter(user__username=username)
        paginated = Paginator(new_posts, 10)

        page_number = request.GET.get("page", 1)
        page_obj = paginated.get_page(page_number)
        return render(
            request,
            "network/profile.html",
            {
                "posts": page_obj,
                "username": username,
                "followers": len(target_user.followers.all()),
            },
        )
    return render(
        request,
        "network/profile.html",
        {
            "posts": page_obj,
            "followers": len(target_user.followers.all()),
        },
    )


@login_required(redirect_field_name="", login_url="login")
def following_view(request, username):
    current_user = request.user
    posts = New_Post.objects.filter(user__in=current_user.following.all())
    if current_user.username != username:
        # TODO: Have an error message or sorts show up here
        return redirect("index")

    return render(
        request,
        "network/following.html",
        {"following": posts},
    )


@csrf_exempt
def follow_unfollow(request, username):
    current_user = request.user
    target_user = User.objects.get(username=username)
    if current_user in target_user.followers.all():
        current_user.following.remove(target_user)
    else:
        current_user.following.add(target_user)
    return JsonResponse({"message": "Successfully followed!"}, status=200)


def get_followers(request, username):
    target_user = User.objects.get(username=username)
    return JsonResponse({"followers": len(target_user.followers.all())})


@csrf_exempt
@login_required(redirect_field_name="", login_url="login")
def like_post(request, id):
    current_user = request.user
    target_post = New_Post.objects.filter(id=id).get()

    if current_user in target_post.likes.all():
        current_user.like.remove(target_post)
    else:
        current_user.like.add(target_post)

    return JsonResponse({"message": "Post liked!"}, status=200)


def get_likes(request, id):
    target_post = New_Post.objects.filter(id=id)
    return JsonResponse({"likes": len(target_post.get().likes.all())})
