# coding=utf-8
async def log(msg):
    print(msg)


class AsyncContextManager:
    async def __aenter__(self):
        await log('entering context')

    async def __aexit__(self, exc_type, exc, tb):
        await log('exiting context')


async def coro():
    async with AsyncContextManager():
        print('body')


c = coro()

try:
    c.send(None)
except StopIteration:
    print('finished')
