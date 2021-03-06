from django.db import models
from django.conf import settings
from random import randint

# Create your models here.

User = settings.AUTH_USER_MODEL


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    # id = models.AutoField(primary_key = True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # one user may have multiple tweets
    content = models.TextField(blank=True, null=True)
    image_path = models.FileField(upload_to="images/", blank=True, null=True)
    likes = models.ManyToManyField(
        User, related_name="Tweet_user", blank=True, through=TweetLike
    )
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": randint(0, 500),
        }

    # def __str__(self):
    #     return self.content
