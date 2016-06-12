# coding=utf-8
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='ceil_cy',
    ext_modules=cythonize('ceil_cy.pyx'),
)
