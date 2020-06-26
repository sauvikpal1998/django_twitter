from django.shortcuts import render
from django.shortcuts import HttpResponse, Http404
from django.http import JsonResponse

from .models import Tweet

import random

# Create your views here.


def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>hello world</h1>")
    return render(request, "pages/home.html", context={}, status=200)


def tweet_list_view(request, *qrgs, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [
        {"id": x.id, "content": x.content, "likes": random.randint(0, 100)} for x in qs
    ]
    status = 200
    data = {"response": tweets_list}
    return JsonResponse(data, status=status)


def tweet_detail_view(request, tweet_id, *args, **kwargs):

    """
    REST API VIEW
    Return JSON
    """

    data = {"id": tweet_id}

    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        data["message"] = "Id not found"
        status = 404

    return JsonResponse(data, status=status)
