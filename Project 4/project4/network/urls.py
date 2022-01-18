
from asyncio import run_coroutine_threadsafe
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.get_profile, name="profile"),

    # API routes
    path("posts", views.compose, name="compose"),
    path("posts/<str:writer>", views.get_posts, name="get_posts"),
    path("posts/edit/<int:post_id>", views.edit_post, name="edit_post"),
]




