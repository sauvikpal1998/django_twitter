from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, Http404
from django.http import JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from .forms import TweetForm
from .models import Tweet

import random

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def tweet_create_view(request, *args, **kwargs):
    print("ajax", request.is_ajax())
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        #  do other form related logic
        obj.save()

        if request.is_ajax():
            return JsonResponse({}, status=201)  # 201 is for create items
        # reinitialize a new form

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)

        form = TweetForm()
    return render(request, "components/form.html", context={"form": form})


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
