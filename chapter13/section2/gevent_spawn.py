# coding=utf-8
import gevent


def a():
    print 'Start a'
    gevent.sleep(1)
    print 'End a'


def b():
    print 'Start b'
    gevent.sleep(2)
    print 'End b'

gevent.joinall([
    gevent.spawn(a),
    gevent.spawn(b),
])
