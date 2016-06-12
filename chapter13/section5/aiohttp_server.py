# coding=utf-8
import json
import asyncio

import aiohttp
from aiohttp import web

REQEUST_URLS = [
    'http://httpbin.org/ip',
    'http://httpbin.org/user-agent',
    'http://httpbin.org/headers'
]


async def handle(request):
    coroutines = [aiohttp.request('get', url) for url in REQEUST_URLS]

    results = await asyncio.gather(*coroutines, return_exceptions=True)

    response_data = {
        url: not isinstance(result, Exception) and result.status == 200
        for url, result in zip(REQEUST_URLS, results)
    }

    body = json.dumps(response_data).encode('utf-8')
    return web.Response(body=body, content_type="application/json")

loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
app.router.add_route('GET', '/', handle)

server = loop.create_server(app.make_handler(), '0.0.0.0', 8081)
print('Server started at http://127.0.0.1:8080')
loop.run_until_complete(server)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
