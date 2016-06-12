# coding=utf-8
from setuptools import setup

setup(
    name='flake8-mc',
    version='0.1.0',
    description='',
    long_description='',
    keywords='flake8 mc checker',
    author='Dong Weiming',
    author_email='dongweiming@dongwm.com',
    url='https://github.com/dongweiming/flake8-mc',
    py_modules=['flake8_mc'],
    zip_safe=False,
    entry_points={
        'flake8.extension': [
            'flake8_mc = flake8_mc:McChecker',
        ],
    },
    install_requires=['flake8'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance'
    ],
)
