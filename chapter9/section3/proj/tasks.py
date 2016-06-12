# coding=utf-8
from __future__ import absolute_import

from celery.utils.log import get_task_logger

from proj.celery import app

logger = get_task_logger(__name__)


@app.task
def add(x, y):
    return x + y


@app.task(bind=True)
def div(self, x, y):
    logger.info(('Executing task id {0.id}, args: {0.args!r} '
                 'kwargs: {0.kwargs!r}').format(self.request))
    try:
        result = x / y
    except ZeroDivisionError as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)
    return result
