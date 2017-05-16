from django.db import models


class Comment(models.Model):

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    text = models.TextField(unique=True, blank=False, null=False)
    user = models.CharField(max_length=45)
    news = models.ForeignKey('News')

    def __str__(self):
        return self.text


class News(models.Model):

    class Meta:
        verbose_name = "new"
        verbose_name_plural = "news"

    url = models.URLField(unique=True)
    site = models.URLField()

    def __str__(self):
        return self.url
