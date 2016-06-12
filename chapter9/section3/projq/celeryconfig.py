# coding=utf-8
from kombu import Queue

BROKER_URL = 'amqp://dongwm:123456@localhost:5672/web_develop'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

CELERY_QUEUES = (
    Queue('default', routing_key='task.#'),
    Queue('web_tasks', routing_key='web.#'),
)
CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'

CELERY_ROUTES = {
    'projq.tasks.add': {
        'queue': 'web_tasks',
        'routing_key': 'web.add',
    }
}
