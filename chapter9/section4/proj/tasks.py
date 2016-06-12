# coding=utf-8
from __future__ import absolute_import

from celery.contrib import rdb

from proj.celery import app


@app.task
def add(x, y):
    return x + y


@app.task(bind=True)
def div(self, x, y):
    try:
        result = x / y
    except ZeroDivisionError as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)
    return result


@app.task
def sub(x, y):
    result = x - y
    rdb.set_trace()  # 设置断点
    return result
