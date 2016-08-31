# coding: utf-8

from django.db import models

from web_scraping.models import Comment


class Annotation(models.Model):

    class Meta:
        verbose_name = "Annotation"
        verbose_name_plural = "Annotations"

    comment = models.ForeignKey(Comment)
    is_hate_speech = models.BooleanField(help_text='Este comentários representa um dicursso de ódio?')
    kind = models.ManyToManyField('KindOfOffence')

    def kinds(self):
        kinds = ""
        for kind in self.kind.values():
            kinds += kind['name'] + ", "
        return kinds

    def __str__(self):
        return str(self.is_hate_speech) + ' - ' + str(list(value['name'] for value in self.kind.values())) + ' - ' + self.comment.text


class KindOfOffence(models.Model):

    class Meta:
        verbose_name = "Kind of Offence"
        verbose_name_plural = "Kind of Offences"

    name = models.CharField(max_length=45)
    definition = models.TextField()

    def __str__(self):
        return self.name 
