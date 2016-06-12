# coding=utf-8
import json
from datetime import date, datetime
from singledispatch import singledispatch
from functools import update_wrapper


def methdispatch(func):
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


def json_serial(obj):
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    TypeError(repr(obj) + ' is not JSON serializable')


class Board(object):
    def __init__(self, id, name, create_at=None):
        self.id = id
        self.name = name
        if create_at is None:
            create_at = datetime.now()
        self.create_at = create_at

    def to_dict(self):
        return {'id': self.id, 'name': self.name,
                'create_at': self.create_at}

    @methdispatch
    def get(self, arg):
        return getattr(self, arg, None)

    @get.register(list)
    def _(self, arg):
        return [self.get(x) for x in arg]


@singledispatch
def json_encoder(obj):
    raise TypeError(repr(obj) + ' is not JSON serializable')


@json_encoder.register(date)
@json_encoder.register(datetime)
def encode_date_time(obj):
    return obj.isoformat()


board = Board(1, 'board_1')

print(json.dumps(board.to_dict(), default=json_encoder))
print(board.get('name'))
print(board.get(['id', 'create_at']))
