# coding=utf-8
"""
Flask-RESTful2
-------------

A new framework for creating REST APIs
"""
from setuptools import setup

setup(
    name='Flask-RESTful2',
    version='0.1',
    url='https://github.com/dongweiming/flask-restful2',
    license='BSD',
    author='Dong Weiming',
    author_email='ciici23@gmail.com',
    description='Simple framework for creating REST APIs',
    long_description=__doc__,
    py_modules=['flask_restful2'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-RESTful==0.3.5'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
