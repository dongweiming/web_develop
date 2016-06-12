# coding=utf-8
from __future__ import unicode_literals

import cPickle as pickle
from time import sleep

import redis
from IPython.display import display
from ipywidgets import widgets


class RedisWrapper(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379)

    def __getattr__(self, attr):
        if attr == 'r':
            return vars(self)['r']
        return pickle.loads(self.r.get(attr))

    def __setattr__(self, key, value):
        if key == 'r':
            vars(self)['r'] = value
        else:
            pickled_object = pickle.dumps(value)
            self.r.set(key, pickled_object)

r = RedisWrapper()


def get_btn(desc):
    return widgets.Button(description="提交{}修改".format(desc))


def hide_btn(btn):
    print('提交完成')
    btn.visible = False
    sleep(1.5)
    btn.visible = True


def set_review():
    '''修改图文'''
    def review_func(btn):
        _review_ids = [
            review_container.children[i].value for i in range(3)]
        r.review_ids = _review_ids
        hide_btn(btn)

    review_container = widgets.Box()
    btn = get_btn("图文")
    children = []
    for o in range(3):
        c = widgets.Text(description="第{}条图文ID".format(o + 1))
        c.value = str(r.review_ids[o])
        children.append(c)
    children.append(btn)
    review_container.children = children
    btn.on_click(review_func)
    display(review_container)


def set_doulist():
    '''修改豆列推荐位'''
    def doulist_func(btn):
        doulists = []
        for i in range(2):
            doulist = []
            doulist_id = doulist_container.children[i].children[0].value
            doulist.append(doulist_id)
            _stories = []
            for p in range(1, 6):
                _stories.append(
                    doulist_container.children[i].children[p].value)
            doulist.append(_stories)
            doulists.append(doulist)
        r.promo_ids = doulists
        hide_btn(btn)

    doulist_container = widgets.Box()
    btn = get_btn("豆列推荐位")
    children = []
    for doulist_id, stories_ids in r.promo_ids:
        doulist = widgets.Box()
        _children = []
        c = widgets.Text(description="豆列ID")
        c.value = str(doulist_id)
        _children.append(c)
        for sid in stories_ids:
            c = widgets.Text()
            c.value = str(sid)
            _children.append(c)
        doulist.children = _children
        children.append(doulist)
    children.append(btn)
    doulist_container.children = children
    btn.on_click(doulist_func)
    display(doulist_container)
    doulist_container._dom_classes = ('doulist',)
#    doulist_container.add_class('doulist')


def set_boards():
    '''修改故事推荐位'''
    def board_func(btn):
        boards = []
        for i in range(3):
            board = []
            for p in range(2):
                try:
                    board.append(
                        int(board_container.children[i].children[p].value))
                except ValueError:
                    board.append(
                        board_container.children[i].children[p].value.encode('utf-8'))  # noqa
            boards.append(board)
        r.boards = boards
        r.promo_title = board_container.children[3].value.encode('utf-8')
        r.promo_subtitle = board_container.children[4].value.encode('utf-8')
        hide_btn(btn)

    board_container = widgets.Box()
    btn = get_btn("故事推荐位")
    children = []
    for o, board in enumerate(r.boards):
        promo = widgets.Box()
        _children = []
        for index, o in enumerate(['StoryID', 'Title']):
            b = board[index]
            if isinstance(b, int):
                b = str(b)
            c = widgets.Text(description=o)
            c.value = b.decode('utf-8')
            _children.append(c)
        promo.children = _children
        children.append(promo)
    promo_title = widgets.Text(description="推荐位标题")
    promo_title.value = r.promo_title.decode('utf-8')
    promo_subtitle = widgets.Text(description="推荐位副标题")
    promo_subtitle.value = r.promo_subtitle.decode('utf-8')
    children.append(promo_title)
    children.append(promo_subtitle)
    children.append(btn)
    board_container.children = children
    btn.on_click(board_func)
    display(board_container)
    board_container._dom_classes = ('board',)
#    board_container.add_class('board')
