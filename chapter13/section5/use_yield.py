# coding=utf-8
import random


def consumer():
    r = None
    while 1:
        data = yield r
        print 'Consuming: {}'.format(data)
        r = data + 1


def producer(consumer):
    n = 3
    consumer.send(None)
    while n:
        data = random.choice(range(10))
        print('Producing: {}'.format(data))
        rs = consumer.send(data)
        print 'Consumer return: {}'.format(rs)
        n -= 1
    consumer.close()


c = consumer()
producer(c)
