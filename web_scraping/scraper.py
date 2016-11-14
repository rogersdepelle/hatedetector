# coding: utf-8

import json
import requests
import time

from datetime import datetime
from lxml import html
from urllib.parse import quote

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


def get_text(tree, path):
    """
    ToDo
    """
    return ''.join(tree.xpath(path))


def get_json(url):
    """
    ToDo
    """
    try:
        return json.loads(requests_get(url).text[28:-1])
    except:
        return []


def comments(script, news):
    """
    Builds the url ajax call that returns the comments in a json,
    save the comments in the database
    :param tree: object with the page's HTML
    :return Boolean: True if the news has reviews and false if not 
    """
    page = 1
    n_comments = 25

    script = script[0].replace("\'", "\"").replace('/', "@@").split("\"")
    param = quote(script[3] + "/" + script[9] + "/" + script[5] + "/" + script[11] + "/" + script[7])
        
    while n_comments == 25:
        response = get_json('http://comentarios.globo.com/comentarios/' + param + '/populares/' + str(page) + '.json')
        if not response['itens']:
            return False

        n_comments = len(response['itens'])
        page += 1

        for comment in response['itens']:
            Comment.objects.create(author=comment['Usuario']['nome'], text=comment['texto'], news=news)
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
                Comment.objects.create(author=reply['Usuario']['nome'], text=reply['texto'], news=news)
    if Comment.objects.filter(news=news).count() > 0:
        return True
    return False


def news(url, date, domain):
    """
    Perform a request in news url, calls comments() to collect comments
    and extract the title, text and date of news.
    :param url: news link
    :return Boolean: True if the news is valid and false if not 
    """
    if News.objects.filter(url=url).exists():
        return False

    paths = ["//*[@id='glb-materia']", "//*[contains(@class, 'corpo-blog')]", "//*[contains(@class, 'widget-comentarios')]"]
    tree = html.fromstring(requests_get(url).text)
    
    for path in paths:
        script = tree.xpath(path + "/script/text()")
        if script:
            break

    if not script:
        return False

    post_blog = tree.xpath("//*[contains(@class, 'corpo-blog')]")
    if post_blog:
        title = get_text(tree, "//*[contains(@class, 'post-title')]/a/text()")
        text = get_text(tree, "//*[contains(@class, 'post-content')]/div/p/text()")
    else:
        title = get_text(tree, "//*[contains(@class, 'materia-titulo')]/h1/text()")
        text = get_text(tree, "//*[contains(@class, 'materia-conteudo')]/div/p/text()")

    if text and title:
        news = News.objects.create(url=url, title=title, text=text, date=date, domain=domain)
    else:
        return False

    if not comments(script, news):
        news.delete()
        return False

    return True


def links(amount, domain):
    """
    Collecting the amount requested links of news domain
    :param amount: number of links
    :param domain: news area
    :return n: number of news collected
    """
    next_page = 1
    n = 0
    while n < amount:
        response = requests_get(domain.url + str(next_page)).json()
        items = response['items']
        for item in items:
            date = item['publication'].split('T')[0]
            date = datetime.strptime(date, '%Y-%m-%d')
            if news(item['content']['url'], date, domain):
                n += 1
                print(n)
            if n == amount:
                break
        next_page = int(response['nextPage'])
    return n
