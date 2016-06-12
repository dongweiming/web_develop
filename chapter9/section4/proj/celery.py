# coding=utf-8
from __future__ import absolute_import

from celery import Celery
from celery.signals import after_task_publish

app = Celery('proj', include=['proj.tasks'])
app.config_from_object('proj.celeryconfig')


@after_task_publish.connect
def task_sent_handler(sender=None, body=None, **kwargs):
    print 'after_task_publish: task_id: {body[id]}; sender: {sender}'.format(
        body=body, sender=sender)


if __name__ == '__main__':
    app.start()
