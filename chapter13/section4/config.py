# coding=utf-8
import re

PROXY_SITES = [
    'http://cn-proxy.com',
    'http://www.xicidaili.com',
    'http://www.kuaidaili.com/free',
    'http://www.youdaili.net/Daili/http/4402.html',
    'http://www.youdaili.net/Daili/http/4403.html',
    'http://www.kuaidaili.com',
    'http://proxy.mimvp.com',
]

REFERER_LIST = [
    'http://www.google.com/',
    'http://www.bing.com/',
    'http://www.baidu.com/',
]

PROXY_REGEX = re.compile('[0-9]+(?:\.[0-9]+){3}:\d{2,4}')

DB_HOST = 'localhost'
DB_PORT = 27017
DATABASE_NAME = 'chapter13'

TIMEOUT = 1
