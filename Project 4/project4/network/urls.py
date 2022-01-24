
from asyncio import run_coroutine_threadsafe
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.get_profile, name="profile"),
    path("followlist", views.get_followed_posts, name="following"),

    # API routes
    path("posts", views.compose, name="compose"),
    path("posts/newpost", views.get_post, name="get_post"),
    path("posts/edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("posts/follows/<str:follow_name>", views.follow_unfollow, name="follow"),
    path("posts/likes/<int:post_id>", views.like_unlike, name="like_unlike"),
]




