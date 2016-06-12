# coding=utf-8
import asyncio
from functools import partial


def set_result(future, result):
    print('Setting future result to {!r}'.format(result))
    future.set_result(result)


def callback(who, future):
    print('[{}]: returned result: {!r}'.format(who, future.result()))


event_loop = asyncio.get_event_loop()
future = asyncio.Future()
future.add_done_callback(partial(callback, 'CB1'))
event_loop.call_soon(set_result, future, 'Done!')
event_loop.call_soon(set_result, future, 'Done again!')
event_loop.run_until_complete(future)
event_loop.close()
