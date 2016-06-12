# coding=utf-8
import urllib
from functools import wraps


def cache(func):
    saved = {}

    @wraps(func)
    def newfunc(*args):
        if args in saved:
            return saved[args]
        result = func(*args)
        saved[args] = result
        return result
    return newfunc


@cache
def web_lookup(url):
    return urllib.urlopen(url).read()


print web_lookup('http://baidu.com')
print web_lookup('http://baidu.com')
