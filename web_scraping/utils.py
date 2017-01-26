# coding: utf-8

import sys

from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.forms import model_to_dict
from django.http import JsonResponse

from annotation.models import Annotation

from .models import Domain, News, Comment
from .scraper import links


def start(n):
    '''
        ToDo
        run: ./manage.py shell -c="from web_scraping.utils import start; start(n)"
    '''
    start = datetime.now()

    try:
        n = int(n)
    except:
        print("Insert number of news")
        return

    domains = Domain.objects.all()

    for d in domains:
        links(n, d)

    print(datetime.now() - start)


@staff_member_required
def dump(request):
    '''
        ToDo
    '''

    news_list = News.objects.all()

    response = []

    for news in news_list:
        response.append(model_to_dict(news, exclude=['id', 'domain']))
        response[-1]['domain'] = news.domain.name
        response[-1]['comments'] = []
        comments = Comment.objects.filter(news=news)
        for comment in comments:
            response[-1]['comments'].append(model_to_dict(comment, exclude=['id', 'news']))

    return JsonResponse(response, safe=False)


def anotar():

    comments = Comment.objects.all()

    for comment in comments:
        annotation = Annotation.objects.filter(comment=comment).exclude(user__id=2)
        rogers = Annotation.objects.get(comment=comment, user__id=2)
        if annotation[0].is_hate_speech == True or annotation[1].is_hate_speech == True:
            rogers.is_hate_speech = True
            for a in annotation[1].kind.all():
                rogers.kind.add(a)
            rogers.save()
        else:
            rogers.is_hate_speech = False
            rogers.save()
