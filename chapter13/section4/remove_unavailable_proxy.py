# coding=utf-8
from functools import partial

from concurrent.futures import (ThreadPoolExecutor, ProcessPoolExecutor,
                                as_completed)
from requests.exceptions import RequestException

from utils import fetch
from models import Proxy


def check_proxy(p):
    try:
        fetch('http://baidu.com', proxy=p['address'])
    except RequestException:
        p.delete()
        return False
    return True


def use_thread_pool_executor():
    with ThreadPoolExecutor(max_workers=5) as executor:
        for p in Proxy.objects.all():
            executor.submit(check_proxy, p)


def when_done(p, f):
    print '[{}]: {}'.format(p.address, 'succeed' if f.result() else 'failure')


def use_thread_pool_executor_with_cb():
    with ThreadPoolExecutor(max_workers=5) as executor:
        for p in Proxy.objects.all():
            result = executor.submit(check_proxy, p)
            result.add_done_callback(partial(when_done, p))


def use_process_pool_executor():
    with ProcessPoolExecutor(max_workers=5) as executor:
        executor.map(check_proxy, Proxy.objects.all())


def process_executor_with_completed():
    with ProcessPoolExecutor(max_workers=5) as executor:
        future_tasks = {executor.submit(
            check_proxy, p): p for p in Proxy.objects.all()}
        for future in as_completed(future_tasks):
            p = future_tasks[future]
            try:
                rs = future.result()
            except Exception as exc:
                print 'Receive exception: {}'.format(exc)
            else:
                print '[{}]: {}'.format(
                    p.address, 'succeed' if rs else 'failure')

process_executor_with_completed()
