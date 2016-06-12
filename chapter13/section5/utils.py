# coding=utf-8
import random

import aiohttp
from fake_useragent import UserAgent

from config import REFERER_LIST, TIMEOUT


def get_referer():
    return random.choice(REFERER_LIST)


def get_user_agent():
    ua = UserAgent()
    return ua.random


async def fetch(url, proxy=None):
    conn = aiohttp.ProxyConnector(proxy=proxy)
    headers = {'user-agent': get_user_agent()}
    with aiohttp.ClientSession(connector=conn) as session:
        with aiohttp.Timeout(TIMEOUT):
            async with session.get('http://python.org', headers) as resp:
                return resp.json()
