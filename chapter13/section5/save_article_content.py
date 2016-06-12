# coding=utf-8
import urllib
import asyncio
from asyncio import TimeoutError
from urllib.parse import urlparse, urlsplit, parse_qs, urlencode
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup

from config import TIMEOUT
from utils import get_user_agent
from models import Proxy, Article, Comment

COMMENT_JS_URL = 'http://mp.weixin.qq.com/mp/getcomment'


class CrawlerError(Exception):
    pass


def gen_js_url(url):
    query_dct = parse_qs(urlsplit(url).query)
    query_dct = {k: v[0] for k, v in query_dct.items()}
    query_dct.update({'uin': '', 'key': '', 'pass_ticket': '', 'wxtoken': '',
                      'devicetype': '', 'clientversion': 0, 'x5': 0})
    return '{}?{}'.format(COMMENT_JS_URL, urlencode(query_dct))


async def fetch(url, retry=0):
    proxy = 'http://{}'.format(Proxy.get_random()['address'])
    headers = {'user-agent': get_user_agent()}
    conn = aiohttp.ProxyConnector(proxy=proxy)

    js_url = gen_js_url(url)

    try:
        with aiohttp.ClientSession(connector=conn) as session:
            with aiohttp.Timeout(TIMEOUT):
                async with session.get(url, headers=headers) as resp:
                    html_text = await resp.text()

                async with session.get(js_url, headers=headers) as resp:
                    js_data = await resp.json()
    except:
        retry += 1
        if retry > 5:
            raise CrawlerError()
        await asyncio.sleep(1)
        return await fetch(url, retry=retry)
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


async def update_article(article, html_text, js_data):
    soup = BeautifulSoup(html_text, 'lxml')
    p_contents = soup.find(class_='rich_media_content').find_all('p')
    content = []
    pictures = {}
    picture_count = 1
    for p_content in p_contents:
        img = p_content.find('img')
        if img is None:
            content.append(p_content.text)
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


async def save_article_result(article, queue=None):
    url = article.article_url

    try:
        html_text, js_data = await fetch(url)
    except CrawlerError:
        queue.put(url)
        return
    return await update_article(article, html_text, js_data)


async def save_article_result_with_queue(queue):
    while 1:
        article = await queue.get()
        if article is None:
            queue.task_done()
            break
        await save_article_result(article, queue)
        queue.task_done()


async def producer(queue):
    for article in Article.objects.all()[20:26]:
        await queue.put(article)

    for i in range(5):
        await queue.put(None)

    await queue.join()


def main():
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    consumers = [
        loop.create_task(save_article_result_with_queue(queue,))
        for i in range(5)
    ]
    prod = loop.create_task(producer(queue))
    loop.run_until_complete(
        asyncio.wait(consumers + [prod])
    )
