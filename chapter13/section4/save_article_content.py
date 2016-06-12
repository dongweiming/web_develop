# coding=utf-8
import urlparse
import urllib
from datetime import datetime
import multiprocessing
from Queue import Empty

import requests
from mongoengine.connection import disconnect
from simplejson.scanner import JSONDecodeError
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from config import TIMEOUT
from utils import get_user_agent
from models import Proxy, Article, Comment, lazy_connect

COMMENT_JS_URL = 'http://mp.weixin.qq.com/mp/getcomment'


def gen_js_url(url):
    query_dct = urlparse.parse_qs(urlparse.urlsplit(url).query)
    query_dct = {k: v[0] for k, v in query_dct.items()}
    query_dct.update({'uin': '', 'key': '', 'pass_ticket': '', 'wxtoken': '',
                      'devicetype': '', 'clientversion': 0, 'x5': 0})
    return '{}?{}'.format(COMMENT_JS_URL, urllib.urlencode(query_dct))


def fetch(url):
    s = requests.Session()
    s.headers.update({'user-agent': get_user_agent()})
    proxies = {
        'http': Proxy.get_random()['address'],
    }
    html_text = s.get(url, timeout=TIMEOUT, proxies=proxies).text
    js_url = gen_js_url(url)
    try:
        js_data = s.get(js_url, timeout=TIMEOUT, proxies=proxies).json()
    except JSONDecodeError:
        raise RequestException()
    return html_text, js_data


def get_comments(js_data, article):
    comments = []
    for comment in js_data['comment']:
        comment_id = comment['id']
        content = comment['content']
        create_at = datetime.fromtimestamp(float(comment['create_time']))
        nick_name = comment['nick_name']
        like_num = comment['like_num']
        comment = Comment.get_or_create(
            article, comment_id, content=content, create_at=create_at,
            nick_name=nick_name, like_num=like_num)
        comments.append(comment)
    return comments


def update_article(article, html_text, js_data):
    soup = BeautifulSoup(html_text, 'lxml')
    p_contents = soup.find(class_='rich_media_content').find_all('p')
    content = []
    pictures = {}
    picture_count = 1
    for p_content in p_contents:
        img = p_content.find('img')
        if img is None:
            content.append(p_content.text.encode('utf-8'))
        else:
            tag = '<图片{}>'.format(picture_count)
            content.append(tag)
            pictures[tag] = img['data-src']
            picture_count += 1

    article.content = '\n'.join(content)
    article.pictures = pictures
    article.comments = get_comments(js_data, article)
    article.like_num = js_data['like_num']
    article.read_num = js_data['read_num']
    article.save()
    return article


def save_article_result(article, queue=None, retry=0):
    url = article.article_url

    try:
        html_text, js_data = fetch(url)
    except RequestException:
        retry += 1
        if retry > 5:
            queue.put(url)
            print '1'
            return
        return save_article_result(article, queue, retry)
    return update_article(article, html_text, js_data)


def save_article_result_with_queue(queue):
    disconnect()
    lazy_connect()
    while 1:
        try:
            article = queue.get(timeout=1)
        except Empty:
            break
        save_article_result(article, queue)
        queue.task_done()


def use_multiprocessing_with_queue():
    queue = multiprocessing.JoinableQueue()
    num_consumers = multiprocessing.cpu_count() * 2

    for article in Article.objects.all():
        queue.put(article)

    for _ in range(num_consumers):
        p = multiprocessing.Process(target=save_article_result_with_queue,
                                    args=(queue,))
        p.start()

    queue.join()


def save_article_result_with_queue2(in_queue, out_queue):
    while 1:
        try:
            article = in_queue.get(timeout=1)
        except Empty:
            break
        updated_article = save_article_result(article, in_queue)
        out_queue.put(updated_article)
        in_queue.task_done()


def use_multiprocessing_with_queue2():
    queue = multiprocessing.JoinableQueue()
    num_consumers = multiprocessing.cpu_count() * 2
    results_queue = multiprocessing.Queue()

    for article in Article.objects.all():
        queue.put(article)

    for _ in range(num_consumers):
        p = multiprocessing.Process(target=save_article_result_with_queue2,
                                    args=(queue, results_queue))
        p.start()

    queue.join()

    results = []

    while 1:
        try:
            updated_article = results_queue.get(timeout=1)
        except Empty:
            break
        results.append(updated_article)
    print len(results)
