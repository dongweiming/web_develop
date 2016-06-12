# coding=utf-8
import asyncio
from asyncio import TimeoutError
from urllib.parse import urlsplit, parse_qs, urlencode

import aiohttp
from aiohttp import ProxyConnectionError
from mongoengine import DoesNotExist

from models import Proxy
from config import TIMEOUT
from utils import get_user_agent


async def fetch(retry=0):
    proxy = 'http://{}'.format(Proxy.get_random()['address'])
    headers = {'user-agent': get_user_agent()}
    conn = aiohttp.ProxyConnector(proxy=proxy)

    url = 'http://httpbin.org/ip'

    try:
        with aiohttp.ClientSession(connector=conn) as session:
            with aiohttp.Timeout(TIMEOUT):
                async with session.get(url, headers=headers) as resp:
                    return await resp.json()
    except (ProxyConnectionError, TimeoutError):
        try:
            p = Proxy.objects.get(address=proxy)
            if p:
                p.delete()
        except DoesNotExist:
            pass
        retry += 1
        if retry > 5:
            raise TimeoutError()
        await asyncio.sleep(1)
        return await fetch(retry=retry)


loop = asyncio.get_event_loop()
f = asyncio.wait([fetch()])
completed, pending = loop.run_until_complete(f)

for future in completed:
    print(future.result())
