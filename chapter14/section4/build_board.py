# coding=utf-8
import os

from cffi import FFI

ffi = FFI()
here = os.path.dirname(__file__)

with open(os.path.join(here, 'board.h')) as f:
    header = f.read().strip()

with open(os.path.join(here, 'board.c')) as f:
    source = f.read().strip()


ffi.set_source('_board', '\n'.join([header, '', source]))
ffi.cdef(header)


if __name__ == "__main__":
    ffi.compile()
