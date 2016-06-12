# coding=utf-8
import random
import asyncio


class AsyncIterable:
    def __init__(self):
        self.count = 0

    async def __aiter__(self):
        return self

    async def __anext__(self):
        if self.count >= 5:
            raise StopAsyncIteration
        data = await self.fetch_data()
        self.count += 1
        return data

    async def fetch_data(self):
        return random.choice(range(10))

async def main():
    async for data in AsyncIterable():
        print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
