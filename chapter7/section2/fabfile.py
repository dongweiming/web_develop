# coding=utf-8
from fabric.api import run, local


def hostname():
    run('hostname')


def ls(path='.'):
    local('ls {}'.format(path))
