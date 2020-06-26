from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("tweets/<int:tweet_id>", views.tweet_detail_view, name="tweet_detail_view"),
    path("tweets/list", views.tweet_list_view, name="tweet_list_view"),
    path("tweets/create_tweet", views.tweet_create_view, name="tweet_create_view"),
]
