from django.urls import path
from . import views



urlpatterns = [
    path("search/", views.search, name="search"),
    path("", views.home, name="home"),
    path("json/", views.listing_api, name="terms-api"),
]