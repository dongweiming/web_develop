# coding=utf-8
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='levenshtein_cy',
    ext_modules=cythonize('levenshtein_cy.pyx'),
)
