# coding=utf-8
from __future__ import absolute_import

from projq.celery import app


@app.task
def add(x, y):
    return x + y
