# coding=utf-8
from mongoengine import (connect, StringField, DateTimeField, ReferenceField,
                         DictField, IntField, ListField, Document,
                         DoesNotExist)

from config import DB_HOST, DB_PORT, DATABASE_NAME


def lazy_connect():
    connect(DATABASE_NAME, host=DB_HOST, port=DB_PORT)

lazy_connect()


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


class Comment(BaseModel):
    nick_name = StringField(max_length=120)
    content = StringField(max_length=120, required=True)
    like_num = IntField()
    comment_id = IntField()
    article = ReferenceField('Article', dbref=True)

    meta = {
        'collection': 'comment',
        'indexes': [
            {'fields': ['article', 'comment_id'],
             'unique': True}
        ]
    }

    @classmethod
    def get_or_create(cls, article, comment_id, **kwargs):
        comments = cls.objects.filter(article=article,
                                      comment_id=comment_id)
        if comments:
            return comments[0]
        comment = cls(article=article, comment_id=comment_id, **kwargs)
        comment.save()
        return comment


class Article(BaseModel):
    title = StringField(max_length=120, required=True)
    img_url = StringField()
    article_url = StringField(required=True)
    summary = StringField()
    publisher = ReferenceField(Publisher, required=True)
    content = StringField()
    pictures = DictField()
    comments = ListField(ReferenceField(Comment))
    like_num = IntField()
    read_num = IntField()

    meta = {
        'collection': 'article',
        'indexes': [
            '-create_at',
            {'fields': ['title', 'summary', 'publisher'],
             'unique': True}
        ],
        'ordering': ['-create_at']
    }
