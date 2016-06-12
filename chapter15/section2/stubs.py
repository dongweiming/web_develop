# coding=utf-8
from mock import Mock

MC_DEFAULT_EXPIRE = 60 * 30


def side_effect(sql, *args):
    sql = sql.lower()
    if 'select' in sql:
        return ((1, 101, 120, 130),)
    else:
        return True


def _store():
    mock = Mock()
    cursor = mock.connection.cursor.return_value
    cursor.execute.side_effect = side_effect
    return cursor

store = _store()


def cache(key_pattern, expire=MC_DEFAULT_EXPIRE):
    def deco(f):
        def _(*a, **kw):
            return f(*a, **kw)
        return _
    return deco


def mc_delete(key_pattern):
    return True
