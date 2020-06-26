from django.db import models

from random import randint

# Create your models here.


class Tweet(models.Model):
    # id = models.AutoField(primary_key = True)
    content = models.TextField(blank=True, null=True)
    image_path = models.FileField(upload_to="images/", blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": randint(0, 500),
        }
