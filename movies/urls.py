from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.movie_search, name="search"),
    path("movies/<slug:slug>/", views.movie_detail, name="movie_detail"),
    path("movies/<slug:slug>/download/", views.movie_download, name="movie_download"),
]
