# coding=utf-8
from libc.math cimport ceil

cpdef double f2(double x):
    return ceil(x)