# coding=utf-8
from functools import partialmethod

DEFAULT_SITE = 'https://www.douban.com'


class Request(object):
    default_url = DEFAULT_SITE

    def request(self, method, url, params=None, data=None):
        print('execute request: {}'.format(url))

    get = partialmethod(request, 'GET')
    post = partialmethod(request, 'POST')

    get_default_url = partialmethod(get, default_url)


req = Request()
req.get('http://sina.com.cn')
req.get_default_url()
