# coding: utf-8

import sys

from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.forms import model_to_dict
from django.http import JsonResponse

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
