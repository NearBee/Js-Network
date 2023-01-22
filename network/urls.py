from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("<str:username>/following", views.following_view, name="following"),
    path(
        "follow_unfollow/<str:username>", views.follow_unfollow, name="follow_unfollow"
    ),
    path("get_followers/<str:username>", views.get_followers, name="get_followers"),
    path("like_post/<int:id>", views.like_post, name="like_post"),
    path("get_likes/<int:id>", views.get_likes, name="get_likes"),
]
