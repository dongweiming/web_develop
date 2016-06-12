# coding=utf-8
import requests


def api_request(url):
    r = requests.get(url)
    return r.json()


def get_review_author(url):
    rs = api_request(url)
    return rs['review']['author']
