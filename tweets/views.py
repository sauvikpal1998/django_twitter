from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, Http404
from django.http import JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import random

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


@api_view(["POST"])  # http method only POST
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        obj = serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(["GET"])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(
    ["delete", "POST"]
)  # delete gives the option for deleting in browser json api renderer
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({"message": "Tweet not found"}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet Removed"}, status=200)


def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=403)
        return redirect(settings.LOGIN_URL)

    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None

    if form.is_valid():
        obj = form.save(commit=False)
        #  do other form related logic
        obj.user = request.user or None
        obj.save()

        # check for ajax request
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)  # 201 is for create items

        # check for redirect link
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)

        # reinitialize a new form
        form = TweetForm()

    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    return render(request, "components/form.html", context={"form": form})


def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>hello world</h1>")
    return render(request, "pages/home.html", context={}, status=200)


def tweet_list_view_pure_django(request, *qrgs, **kwargs):
    qs = Tweet.objects.all()
    # tweets_list = [
    #     {"id": x.id, "content": x.content, "likes": random.randint(0, 100)} for x in qs
    # ]

    tweets_list = [x.serialize() for x in qs]

    status = 200
    data = {"response": tweets_list}
    return JsonResponse(data, status=status)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):

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
