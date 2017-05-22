# coding: utf-8

import re

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse


from comments.models import Comment
from dashboard.utils import set_context as st

from .models import Annotation, Annotator, KindOfOffence
from .forms import AnnotationForm, AnnotatorForm


def set_context(request):
    context = st(request)
    context['meta'] = Comment.objects.all().count()
    context['types'] = KindOfOffence.objects.all()
    return context


def home(request):
    context = set_context(request)
    #context['neg'], context['pos'] = Annotation.status()
    context['neg'] = 0
    context['pos'] = 0
    context['unclas'] = context['meta'] -context['neg'] - context['pos']
    return render(request, "home.html", context)


def congrat(request):
    context = set_context(request)
    return render(request, "congrat.html", context)


def start(request):
    context = set_context(request)

    if request.POST:
        request.session['pretest'] = 0
        try:
            request.session['annotator'] = Annotator.objects.get(email=request.POST['email']).email
            return redirect('annotation')
        except:
            form = AnnotatorForm(request.POST)
            if form.is_valid():
                request.session['annotator'] = form.save().email
                return redirect('annotation')
    else:
        form = AnnotatorForm()

    context['form'] = form

    return render(request, "start.html", context)


def annotation(request):
    context = set_context(request)

    try:
        annotator = Annotator.objects.get(email=request.session['annotator'])
    except:
        return redirect('home')

    if annotator.approved == False:
        return redirect('congrat')

    if annotator.approved:
        comment, end = annotator.get_available()
        if end:
          return redirect('congrat')

    elif annotator.approved == None:
        annotations = Annotation.get_pretest()
        if int(request.session['pretest']) == len(annotations):
            annotator.rating()
            return redirect('annotation')
        else:
            annotation = annotations[request.session['pretest']]
            comment = annotation.comment

    if request.POST:
        form = AnnotationForm(request.POST)
        if form.is_valid():
            form.save(annotator=annotator, comment=comment)
            request.session['pretest'] += 1
            return redirect('annotation')
    else:
        form = AnnotationForm()

    context['form'] = form
    context['comment'] = comment
    context['annotation_n'] = Annotation.objects.filter(annotator=annotator).count()

    return render(request, "annotation.html", context)


@staff_member_required
def dashboard(request):
    context = set_context(request)
    context['neg'], context['pos'] = Annotation.status()
    context['unclas'] = context['meta'] -context['neg'] - context['pos']
    context['n_annotations'] = Annotation.objects.all().count()
    context['n_annotators']= Annotator.objects.filter(approved=True).count()
    return render(request, "dashboard.html", context)


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

