# coding=utf-8
from __future__ import absolute_import

from celery import Celery

app = Celery('projq', include=['projq.tasks'])
app.config_from_object('projq.celeryconfig')


if __name__ == '__main__':
    app.start()
