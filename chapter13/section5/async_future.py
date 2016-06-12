# coding=utf-8
import asyncio

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Done!')


loop = asyncio.get_event_loop()
future = asyncio.Future()
print('Future Done: {}'.format(future.done()))
asyncio.ensure_future(slow_operation(future))
loop.run_until_complete(future)
print('Future Done: {}'.format(future.done()))
print(future.result())
loop.close()
