# coding: utf-8

import csv
import re

from unicodedata import normalize

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse


from web_scraping.models import Comment
from dashboard.utils import set_context

from .models import Annotation, KindOfOffence
from .forms import AddAnnotationForm, AnnotationForm


@login_required(redirect_field_name=None)
def annotation(request):
    context = set_context(request)
    context['types'] = KindOfOffence.objects.all()
    user_annotations = Annotation.objects.filter(user=request.user).order_by('id')
    remaining = user_annotations.filter(is_hate_speech=None)
    context['annotation_n'] = user_annotations.count()
    context['annotation_i'] = context['annotation_n'] - remaining.count()

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
    table = []
    total = {}
    comments = Comment.objects.all()
    users = User.objects.filter(is_superuser=False)
    annotations = Annotation.objects.all()

    for user in users:
        item = {}
        item['user'] = user.get_full_name()
        user_annotations = annotations.filter(user=user)
        item['classifications'] = user_annotations.count()
        item['positive'] = user_annotations.filter(is_hate_speech=True).count()
        item['negative'] = user_annotations.filter(is_hate_speech=False).count()
        item['remaining'] = user_annotations.filter(is_hate_speech=None).count()
        table.append(item)
    total['users'] = users.count()
    total['classifications'] = annotations.count()
    total['positive'] = annotations.filter(is_hate_speech=True).count()
    total['negative'] = annotations.filter(is_hate_speech=False).count()
    total['remaining'] = annotations.filter(is_hate_speech=None).count()
    context['n_valid_comments'] = comments.filter(valid=True).count()
    context['n_comments'] = comments.count()

    if request.POST:
        form = AddAnnotationForm(request.POST)
        if form.is_valid():
            if form.save() > 0:
                return redirect('dashboard')
            else:
                context['msg'] = "Não existem comentários válidos disponíveis."
    else:
        form = AddAnnotationForm()

    kinds = KindOfOffence.objects.all()

    m = {}
    for kind in kinds:
        m[kind.name] = 0


    #3
    comments = Comment.objects.all()
    for comment in comments:
        kinds_list = set(k.name for k in kinds)
        annotations = Annotation.objects.filter(comment=comment)
        for annotation in annotations:
            annotation_list = set(k['name'] for k in annotation.kind.values())
            kinds_list = annotation_list.intersection(kinds_list)
        for k in kinds_list:
            m[k] += 1

    m = {}
    for kind in kinds:
        m[kind.name] = 0

    #2
    comments = Comment.objects.all()
    for comment in comments:
        n = {}
        for kind in kinds:
            n[kind.name] = 0
        annotations = Annotation.objects.filter(comment=comment)
        for annotation in annotations:
            if annotation.is_hate_speech:
                for k in annotation.kind.values():
                    n[k['name']] += 1
        for kind in kinds:
            if n[kind.name] >= 2:
                m[kind.name] += 1


    m = {}
    for kind in kinds:
        m[kind.name] = 0
    #1
    comments = Comment.objects.all()
    for comment in comments:
        annotation_list = set()
        annotations = Annotation.objects.filter(comment=comment)
        for annotation in annotations:
            if annotation.is_hate_speech:
                for k in annotation.kind.values():
                    annotation_list.add(k['name'])
        for k in annotation_list:
            m[k] += 1

    context['form'] = form
    context['table'] = table
    context['total'] = total

    return render(request, "dashboard.html", context)


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


def arff(request):
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
        """
        if s >= 2:
            value = 'yes'
        else:
            value = 'no'
        """
        if s == 0 or s == 3:
            if s == 3:
                value = 'yes'
            elif s == 0:
                value = 'no'
            text = normalize('NFKD',  comment.text).encode('ASCII','ignore').decode('ASCII')
            #text = re.sub("[^a-zA-Z ]", "", text.lower())
            text = re.sub("[^a-zA-Z ]", "", text)
            writer.writerow([value, '\''+text+'\''])
    return responsed


def kappa(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="kappa.csv"'
    comments = Comment.objects.all()

    writer = csv.writer(response)
    for comment in comments:
        annotations = Annotation.objects.filter(comment=comment)
        a = 1 if annotations.get(user__id=2).is_hate_speech else 0
        b = 1 if annotations.get(user__id=3).is_hate_speech else 0
        c = 1 if annotations.get(user_id__gt=3).is_hate_speech else 0
        writer.writerow([a, b, c])
    return response

