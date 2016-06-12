# coding=utf-8
from cffi import FFI
ffi = FFI()

ffi.set_source(
    '_api_out',
    '''
        #include <math.h>
    '''
)

ffi.cdef('double ceil(double x);')


def main():
    ffi.compile()

    from _api_out import lib

    print lib.ceil(10.9)


if __name__ == '__main__':
    main()
