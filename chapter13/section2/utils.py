# coding=utf-8
import random

import requests
from fake_useragent import UserAgent

from config import REFERER_LIST, TIMEOUT


def get_referer():
    return random.choice(REFERER_LIST)


def get_user_agent():
    ua = UserAgent()
    return ua.random


def fetch(url, proxy=None):
    s = requests.Session()
    s.headers.update({'user-agent': get_user_agent()})

    proxies = None
    if proxy is not None:
        proxies = {
            'http': proxy,
        }
    return s.get(url, timeout=TIMEOUT, proxies=proxies)
