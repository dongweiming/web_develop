# coding=utf-8
from fabric.api import (
    cd, run, task, env, roles, put, execute, parallel, hide, settings, sudo)
from fabric.colors import red, green
from fabric.contrib.files import exists

env.roledefs.update({
    'webserver': ['192.168.0.130', '192.168.0.132'],
    'dbserver': ['192.168.0.175']
})


@task
@parallel(pool_size=5)
@roles('webserver', 'dbserver')
def top_mem_proc():
    run('ps -ef |sort -rk4 |head')


@task
@roles('webserver')
def upload():
    put('chapter6/section1/run.py', '/tmp/run.py')


def check_command(cmd):
    rs = run('command -v {} >/dev/null 2>&1'.format(cmd))
    return rs.return_code == 0


@task
def install_it(package):
    sudo('pip install {}'.format(package))
    print green('{} installed'.format(package))


@task
@roles('webserver')
def restart_app():
    with cd('/tmp'):
        if exists('/tmp/app.pid'):
            pid = run('cat /tmp/app.pid')
            run('kill -9 {}; rm /tmp/app.pid'.format(pid))
        else:
            print red('pid file not exists!')
        with settings(hide('everything'), warn_only=True):
            if not check_command('gunicorn'):
                install_it('gunicorn')
        with hide('running', 'stdout'):
            run('gunicorn -w 3 run:app -b 0.0.0.0:8000 -D -p /tmp/app.pid --log-file /tmp/app.log')  # noqa


@task
def deploy():
    execute(upload)
    execute(restart_app)
