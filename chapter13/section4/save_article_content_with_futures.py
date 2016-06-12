# coding=utf-8
from functools import partial

from concurrent.futures import ThreadPoolExecutor

from save_article_content import save_article_result
from models import Article


def use_executor():
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(partial(save_article_result, queue=executor._work_queue),
                     Article.objects.all())
