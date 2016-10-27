# coding: utf-8

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from web_scraping.models import Comment
from dashboard.utils import set_context

from .models import Annotation
from .forms import AddAnnotationForm


@login_required(redirect_field_name=None)
def annotation(request):
    context = set_context(request)
    return render(request, "annotation.html", context)


@staff_member_required
def dashboard(request):
    context = set_context(request)
    table = []
    total = {}
    comments = Comment.objects.all()
    users = User.objects.all()
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
    total['x'] = annotations.filter(is_hate_speech=None).count()

    if request.POST:
        form = AddAnnotationForm(request.POST)
        if form.is_valid():
            if form.save() > 0:
                return redirect('annotation_admin')
            else:
                context['msg'] = "Não existem comentários válidos disponíveis."
    else:
        form = AddAnnotationForm()

    context['form'] = form
    context['n_comments'] = comments.count()
    context['n_valid_comments'] = comments.filter(valid=True).count()
    context['table'] = table

    return render(request, "admin.html", context)
