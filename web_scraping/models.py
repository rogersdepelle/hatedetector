from django.db import models


class Comment(models.Model):

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    author = models.CharField(max_length=45)
    text = models.TextField()
    news = models.ForeignKey('News')
    valid = models.NullBooleanField()

    def __str__(self):
        return self.text


class Domain(models.Model):

    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    url = models.URLField(unique=True)
    name = models.CharField(max_length=45)
    site = models.URLField()

    def __str__(self):
        return self.name


class News(models.Model):

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    url = models.URLField(unique=True)
    title = models.CharField(max_length=250)
    text = models.TextField()
    date = models.DateField()
    domain = models.ForeignKey('Domain')

    def __str__(self):
        return self.title
