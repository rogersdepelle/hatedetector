from django.db import models


class Tweet(models.Model):

    class Meta:
        verbose_name = "Tweet"
        verbose_name_plural = "Tweets"

    lang = models.CharField(max_length=2)
    text = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.text

