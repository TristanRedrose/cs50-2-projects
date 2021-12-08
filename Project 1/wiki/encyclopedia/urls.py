from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.subject, name="title"),
    path("shuf=rnd/random", views.randy, name="randy"),
    path("search/", views.search, name="search"),
    path("create/new-page", views.create, name="create"),
    path("<str:title>/edit", views.edit, name="edit")
]
