# coding=utf-8
from datetime import datetime

from requests.exceptions import Timeout, ConnectionError
from gevent import monkey, sleep, GreenletExit
from gevent.queue import Queue, Empty
from gevent.pool import Pool
from gevent.coros import BoundedSemaphore
monkey.patch_all()
from pymongo.errors import InvalidBSON
from mongoengine import NotUniqueError, DoesNotExist
from bs4 import BeautifulSoup

from utils import fetch
from models import Proxy, Article, Publisher

SEARCH_URL = 'http://weixin.sogou.com/weixin?query={}&type=2&page={}'
SEARCH_TEXT = 'Python'

sem = BoundedSemaphore(1)
IN_POOL_TASKS = []


def put_new_page(p, queue):
    global IN_POOL_TASKS
    sem.acquire()
    sleep(0)
    if p not in IN_POOL_TASKS:
        queue.put(p)
        IN_POOL_TASKS.append(p)
    sem.release()


def save_search_result(page, queue, retry=0):
    proxy = Proxy.get_random()['address']
    url = SEARCH_URL.format(SEARCH_TEXT, page)

    try:
        r = fetch(url, proxy=proxy)
    except (Timeout, ConnectionError, IOError):
        sleep(0.1)
        retry += 1
        if retry > 5:
            put_new_page(page, queue)
            raise GreenletExit()
        try:
            p = Proxy.objects.get(address=proxy)
            if p:
                p.delete()
        except DoesNotExist:
            pass

        return save_search_result(page, queue, retry)
    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.find(class_='results')
    if results is None:
        # 此代理已经被封, 换其他的代理
        sleep(0.1)
        retry += 1
        if retry > 5:
            put_new_page(page, queue)
            print 'retry too much!'
            raise GreenletExit()
        return save_search_result(page, queue, retry)
    articles = results.find_all(
        'div', lambda x: 'wx-rb' in x)
    for article in articles:
        save_article(article)

    page_container = soup.find(id='pagebar_container')
    if page_container and u'下一页' in page_container.text:
        last_page = int(page_container.find_all('a')[-2].text)
        current_page = int(page_container.find('span').text)
        for page in range(current_page + 1, last_page + 1):
            put_new_page(page, queue)


def save_article(article_):
    img_url = article_.find(class_='img_box2').find(
        'img').attrs['src'].split('url=')[1]
    text_box = article_.find(class_='txt-box')
    title = text_box.find('h4').find('a').text
    article_url = text_box.find('h4').find('a').attrs['href']
    summary = text_box.find('p').text
    create_at = datetime.fromtimestamp(float(text_box.find(
        class_='s-p').attrs['t']))
    publisher_name = text_box.find(class_='s-p').find('a').attrs['title']

    article = Article(img_url=img_url, title=title, article_url=article_url,
                      summary=summary, create_at=create_at,
                      publisher=Publisher.get_or_create(publisher_name))
    try:
        article.save()
    except (NotUniqueError, InvalidBSON):
        pass


def cleanup():
    Article.drop_collection()
    Publisher.drop_collection()


def save_search_result_with_queue(queue):
    while 1:
        try:
            p = queue.get(timeout=0)
        except Empty:
            break

        print p, 'page'
        save_search_result(p, queue)
    print 'stopping crawler...'


def use_gevent_with_queue():
    queue = Queue()
    pool = Pool(5)

    for p in range(1, 7):
        put_new_page(p, queue)

    while pool.free_count():
        sleep(0.1)
        pool.spawn(save_search_result_with_queue, queue)

    pool.join()


use_gevent_with_queue()
