# coding: utf-8

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import AddAnnotationForm


@login_required(redirect_field_name=None)
def annotation(request):
    context = {}
    return render(request, "annotation.html", context)


@staff_member_required
def annotation_admin(request):
    context = {}

    if request.POST:
        form = AddAnnotationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('annotation_admin')
    else:
        form = AddAnnotationForm()

    context['form'] = form

    return render(request, "admin.html", context)


def annotation_login(request):
    context = {}
    return render(request, "login.html", context)


def annotation_logout(request):
    logout(request)
    return redirect('annotation_login')
