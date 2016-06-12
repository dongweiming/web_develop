# coding=utf-8
import re
import threading
from multiprocessing.dummy import Pool as ThreadPool

import requests
from mongoengine import NotUniqueError

from models import Proxy
from config import PROXY_REGEX, PROXY_SITES
from utils import fetch


def save_proxies(url):
    try:
        r = fetch(url)
    except requests.exceptions.RequestException:
        return False
    addresses = re.findall(PROXY_REGEX, r.text)
    for address in addresses:
        proxy = Proxy(address=address)
        try:
            proxy.save()
        except NotUniqueError:
            pass


def cleanup():
    Proxy.drop_collection()


def non_thread():
    cleanup()
    for url in PROXY_SITES:
        save_proxies(url)


def use_thread():
    cleanup()
    threads = []
    for url in PROXY_SITES:
        t = threading.Thread(target=save_proxies, args=(url,))
        t.setDaemon(True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def use_thread_pool():
    cleanup()
    pool = ThreadPool(5)
    pool.map(save_proxies, PROXY_SITES)
    pool.close()
    pool.join()
