# coding: utf-8

import csv
import re

from unicodedata import normalize

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse


from comments.models import Comment
from dashboard.utils import set_context as st

from .models import Annotation, KindOfOffence
from .forms import AnnotationForm


def set_context(request):
    context = st(request)
    context['meta'] = Comment.objects.all().count()
    return context


def home(request):
    context = set_context(request)
    return render(request, "home.html", context)

#sem seção redirecionar para home
def start(request):
    context = set_context(request)
    return render(request, "start.html", context)

#sem seção redirecionar para home
def annotation(request):
    context = set_context(request)
    context['types'] = KindOfOffence.objects.all()
    remaining = Annotation.objects.all()
    context['annotation_n'] = 100
    context['annotation_i'] = 45

    if context['annotation_n'] == 0:
        return render(request, "without_notes.html", context)

    if remaining.count() == 0:
        context['classifications'] = user_annotations.count()
        context['positive'] = user_annotations.filter(is_hate_speech=True).count()
        context['negative'] = user_annotations.filter(is_hate_speech=False).count()
        return render(request, "completed.html", context)

    if request.POST:
        form = AnnotationForm(request.POST, instance=remaining[0])
        if form.is_valid():
            form.save()
            return redirect('annotation')
    else:
        form = AnnotationForm(instance=remaining[0])

    context['annotation'] = remaining[0]
    context['form'] = form

    return render(request, "annotation.html", context)


@staff_member_required
def dashboard(request):
    context = set_context(request)
    return render(request, "dashboard.html", context)


@staff_member_required
def export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="comments.csv"'
    comments = Comment.objects.all()

    writer = csv.writer(response)
    writer.writerow(['id', 'a1', 'a2', 'a3', 'text'])

    for comment in comments:
        annotations = Annotation.objects.filter(comment=comment)
        writer.writerow([comment.id, annotations[0].is_hate_speech, annotations[1].is_hate_speech, annotations[2].is_hate_speech, comment.text])

    return response


@staff_member_required
def arff(request, raters=3):
    response = HttpResponse(content_type='text/arff')
    response['Content-Disposition'] = 'attachment; filename="default3.arff"'
    comments = Comment.objects.all()


    writer = csv.writer(response)
    for comment in comments:
        annotations = Annotation.objects.filter(comment=comment)
        s = 0
        for a in annotations:
            if a.is_hate_speech:
                s += 1

        if raters == 2:
            if s >= 2:
                value = 'yes'
            else:
                value = 'no'
        else:
            if s == 0 or s == 3:
                if s == 3:
                    value = 'yes'
                elif s == 0:
                    value = 'no'
        writer.writerow([value, '\''+comment.text+'\''])
    return responsed


def kappa(request):
    return 0.5

