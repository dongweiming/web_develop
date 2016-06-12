# coding=utf-8
from mongoengine import (connect, StringField, DateTimeField, ReferenceField,
                         Document, DoesNotExist)

from config import DB_HOST, DB_PORT, DATABASE_NAME

connect(DATABASE_NAME, host=DB_HOST, port=DB_PORT)


class BaseModel(Document):
    create_at = DateTimeField()

    meta = {'allow_inheritance': True,
            'abstract': True}


class Proxy(BaseModel):
    address = StringField(unique=True)

    meta = {'collection': 'proxy'}

    @classmethod
    def get_random(cls):
        proxy = cls.objects.aggregate({'$sample': {'size': 1}}).next()
        return proxy


class Publisher(BaseModel):
    display_name = StringField(max_length=50, required=True)

    meta = {'collection': 'publisher'}

    @classmethod
    def get_or_create(cls, display_name):
        try:
            return cls.objects.get(display_name=display_name)
        except DoesNotExist:
            publisher = cls(display_name=display_name)
            publisher.save()
            return publisher


class Article(BaseModel):
    title = StringField(max_length=120, required=True)
    img_url = StringField()
    article_url = StringField(required=True)
    summary = StringField()
    publisher = ReferenceField(Publisher, required=True)
    create_at = DateTimeField()

    meta = {
        'collection': 'article',
        'indexes': [
            '-create_at',
            {'fields': ['title', 'summary', 'publisher'],
             'unique': True}
        ],
        'ordering': ['-create_at']
    }
