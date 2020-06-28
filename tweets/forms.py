from django import forms

from .models import Tweet
from django.conf import settings


MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["content"]

    def clean_content(self):
        # self.cleaned_data = super().clean()
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long.")
        return content
