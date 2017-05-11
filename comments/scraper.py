# coding: utf-8

import json
import requests
import re
import time

from lxml import html
from unicodedata import normalize
from urllib.parse import quote
from multiprocessing import Pool

from .models import Comment, News


def requests_get(url='', timeout=0.5):
    """
    Perform the request with GET method.
    :param url: url to request
    :param timeout: timeout to purge request
    :return: content of page
    """
    exception = True
    response = None
    while exception:
        try:
            response = requests.get(url, timeout=timeout)
            exception = False
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            exception = True
        except requests.exceptions.Timeout:
            timeout += 0.1
            exception = True

    return response


def get_json(url):
    """
    ToDo
    """
    try:
        return json.loads(requests_get(url).text[28:-1])
    except:
        return []


def save_comment(text, new, user):

    text = re.sub(r'(https?:\/\/)?(w+\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', '', text)
    text = normalize('NFKD',  text.lower()).encode('ASCII','ignore').decode('ASCII')
    words = re.findall(r'\b((\w[^\w]){3,50}\w)\b', text)
    for word in words:
        word_clean = re.sub("[^a-z]", "", word[0])
        text = text.replace(word[0], word_clean)
    text = re.sub("[^a-z ]", " ", text)
    text = re.sub(r"\b(.)\1{2,}", " ", text)
    text = " ".join(text.split())

    try:
        Comment.objects.create(text=text, news=url, user=user)
    except:
        pass


def g1_get_comments(url):
    #./manage.py shell -c="from comments.scraper import g1_get_comments; g1_get_comments()"

    site = "http://www.globo.com/"
    tree = html.fromstring(requests_get(url).text)
    print(url)

    try:
        script = tree.xpath("//*[@id='SETTINGS']/text()")[0]
    except:
        return

    script = script.replace("\'", "\"").replace('/', "@@")
    title = re.findall(r'TITLE: "(.+)"',script)[0]
    curl = re.findall(r'CANONICAL_URL: "(.+)"',script)[0]
    uri = re.findall(r'COMENTARIOS_URI: "(.+)",COMENTARIOS_IDEXTERNO',script)[0]
    id_externo = re.findall(r'COMENTARIOS_IDEXTERNO: "(.+)",    HOST',script)[0]

    parameters = quote(uri + "/" + id_externo + "/" + curl + "/shorturl/" + title)

    page = 1
    n_comments = 25

    while n_comments == 25:
        new = News.objects.create(url=url, site=site)
        response = get_json('http://comentarios.globo.com/comentarios/' + parameters + '/populares/' + str(page) + '.json')
        if not response['itens']:
            return False

        n_comments = len(response['itens'])
        page += 1

        for comment in response['itens']:
            save_comment(comment['texto'], comment['Usuario']['nome'], url)
            if comment['qtd_replies'] <= 2:
                replies = comment['replies']
            else:
                replies_page = 1
                n_replies = 25
                replies = []
                while n_replies == 25:
                    response = get_json('http://comentarios.globo.com/comentarios/respostas/' + str(comment['idComentario']) + '/' + str(replies_page) + '.json')
                    replies += response['itens']
                    n_replies = len(response['itens'])
                    replies_page += 1

            for reply in replies:
                save_comment(reply['texto'], reply['Usuario']['nome'], url)


def folha_get_comments(id_news = 6050186):
    #./manage.py shell -c="from comments.scraper import folha_get_comments; folha_get_comments()"

    site = "http://www.folha.uol.com.br/"

    while id_news > 0:
        id_news -= 1
        url = "http://comentarios1.folha.uol.com.br/comentarios/"+str(id_news)

        tree = html.fromstring(requests_get(url).text)
        try:
            new = News.objects.create(url=tree.xpath("//*[@class='more-news']//a/@href")[0], site=site)
        except:
            print(id_news)
            continue
        comments = tree.xpath("//*[@id='comments']/li//p[1]/text()")
        names = tree.xpath("//*[@id='comments']/li//h6/span/text()")
        print(comments[1])
        for i in range(0, len(comments)):
            save_comment(comments[i], a, names[i].replace('\n','').replace('\t',''))
            print()
            print()
        return


def g1_get_urls():
    #./manage.py shell -c="from comments.scraper import g1_get_urls; g1_get_urls()"

    domain = "http://falkor-cda.bastian.globo.com/feeds/8d7daa58-07fd-45c9-b1fe-aaa654957850/posts/page/" # G1 Política
    #domain = "http://falkor-cda.bastian.globo.com/feeds/93a4eb4b-8a93-4c09-b080-4ba92a01d142/posts/page/" # Globo Esporte
    #domain = "http://falkor-cda.bastian.globo.com/feeds/e9d5d133-bc15-417d-8722-0f44e23f0f7b/posts/page/" # G1 Economia

    next_page = 1

    while next_page != 0:
        response = requests_get(domain + str(next_page)).json()
        urls = []
        for item in response['items']:
            try:
                urls.append(item['content']['url'])
            except:
                pass
        with Pool(10) as p:
            p.map(g1_get_comments, urls)
        next_page = response['nextPage']
