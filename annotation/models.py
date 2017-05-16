# coding: utf-8

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from comments.models import Comment


class Annotation(models.Model):

    class Meta:
        verbose_name = "Annotation"
        verbose_name_plural = "Annotations"
        unique_together = (("annotator", "comment"),)

    annotator = models.ForeignKey('Annotator')
    comment = models.ForeignKey(Comment)
    is_hate_speech = models.NullBooleanField()
    kind = models.ManyToManyField('KindOfOffence', blank=True)
    other = models.CharField(max_length=45, blank=True)

    def kinds(self):
        kinds = ""
        for kind in self.kind.values():
            kinds += kind['name'] + ", "
        return kinds

    def get_pretest():
        return Annotation.objects.filter(annotator__email="teste@teste.com")

    def status():
        comments = Comment.objects.all()
        pos = 0
        neg = 0

        for comment in comments:
            annotations = Annotation.objects.filter(comment=comment)
            if len(annotations) == settings.N_RATERS:
                yes = 0
                for annotation in annotations:
                    if annotation.is_hate_speech:
                        yes += 1

                if yes >= settings.MIN_AGREEMENT:
                    pos += 1
                else:
                    neg += 1
        return neg, pos

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


class Annotator(models.Model):

    class Meta:
        verbose_name = "Annotator"
        verbose_name_plural = "Annotators"

    email = models.EmailField(unique=True)
    approved = models.NullBooleanField()


    def rating(self):
        annotations = Annotation.get_pretest()
        score = 0
        for annotation in annotations:
            a = Annotation.objects.get(annotator=self, comment=annotation.comment)
            if a.is_hate_speech == annotation.is_hate_speech:
                score += 1
        if float(score)/len(annotations) > 0.7:
            self.approved = True
        else:
            self.approved = False
        self.save()

    def get_available(self):
        comments = Comment.objects.all()
        for comment in comments:
            if Annotation.objects.filter(comment=comment).count() < settings.N_RATERS and Annotation.objects.filter(comment=comment, annotator=self).count() == 0:
                return comment, False
        return [], True

    def __str__(self):
        return self.email

