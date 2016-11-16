from django.shortcuts import render

from dashboard.utils import set_context


def index(request):
    context = set_context(request)
    return render(request, 'index.html', context)


def papers(request):
    context = set_context(request)
    return render(request, 'papers.html', context)


def hatespeech(request):
    context = set_context(request)
    return render(request, 'hatespeech.html', context)


def news(request):
    context = set_context(request)
    return render(request, 'news.html', context)


def contact(request):
    context = set_context(request)
    return render(request, 'contact.html', context)
