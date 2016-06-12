# coding=utf-8

from cffi import FFI

ffi = FFI()
ffi.set_source('_abi_out', None)
ffi.cdef('double ceil(double x);')


def main():
    ffi.compile()

    from _abi_out import ffi as ffi_

    lib = ffi_.dlopen(None)

    print lib.ceil(ffi.cast('float', 10.9))

if __name__ == '__main__':
    main()
