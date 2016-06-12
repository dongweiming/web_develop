# coding=utf-8
from __future__ import absolute_import

from celery import Celery

app = Celery('projb', include=['projb.tasks'])
app.config_from_object('projb.celeryconfig')


if __name__ == '__main__':
    app.start()
