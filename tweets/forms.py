from django import forms

from .models import Tweet


class Tweetform(forms.ModelForm):
    class Meta:
        model = Tweet
        fiels = ["content"]

    def clean_content(self):
        pass
