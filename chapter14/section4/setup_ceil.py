# coding=utf-8
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='ceil',
    ext_modules=cythonize('ceil.pyx'),
)
