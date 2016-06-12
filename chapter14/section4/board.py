# coding=utf-8
from _board import ffi, lib


class Board(object):
    def __init__(self, id, name):
        p = lib.create(id, name)
        if p == ffi.NULL:
            raise MemoryError('Could not allocate board')

        self._p = ffi.gc(p, lib.board_destroy)

    @property
    def id(self):
        return self._p.p_id

    @property
    def name(self):
        return ffi.string(self._p.p_name)


if __name__ == '__main__':
    board = Board(1, u'board_1')
    print 'ID: ', board.id
    print 'Name: ', board.name
