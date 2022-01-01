from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlist", views.newlist, name="newlist"),
    path("listing/<str:listid>", views.list_view, name="listview"),
    path("ctg", views.category_view, name="ctg"),
    path("ctg/<str:catid>", views.category_listview, name="ctgview"),
    path("listing/<str:listid>/close", views.close_list, name="choice"),
    path("watchlist", views.watch, name="watchlist"),
    path("watchdel", views.watchdel, name="watchdel"),
    path("addbid", views.addbid, name="addbid"),
    path("closed_view", views.closed_view, name="closed_view")
]
