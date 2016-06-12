# coding=utf-8
import threading
from contextlib import contextmanager, nested


class LockContext(object):

    def __init__(self):
        print '__init__'
        self.lock = threading.Lock()

    def __enter__(self):
        print '__enter__'
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print '__exit_'
        self.lock.release()

with LockContext():
    print 'In the context'


class OpenContext(object):

    def __init__(self, filename, mode):
        self.fp = open(filename, mode)

    def __enter__(self):
        return self.fp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()


with OpenContext('/tmp/a', 'a') as f:
    f.write('hello world')


@contextmanager
def make_open_context(filename, mode):
    fp = open(filename, mode)
    try:
        yield fp
    finally:
        fp.close()


with make_open_context('/tmp/a', 'a') as f:
    f.write('hello world')


@contextmanager
def make_context(*args):
    print args
    yield


with make_context(1, 2) as A:
    with make_context(3, 4) as B:
        print 'In the context'


with make_context(1, 2) as A, make_context(3, 4) as B:
    print 'In the context'


with nested(make_context(1, 2), make_context(3, 4)) as (A, B):
    print 'In the context'
