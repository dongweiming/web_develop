# coding=utf-8
import os
import sys
from functools import partial
from contextlib import contextmanager


@contextmanager
def suppress(*exceptions):
    try:
        yield
    except exceptions:
        pass


with suppress(OSError):
    os.remove('/no/such/file')


with open('help.txt', 'w') as f:
    oldstdout = sys.stdout
    sys.stdout = f
    try:
        help(pow)
    finally:
        sys.stdout = oldstdout


@contextmanager
def redirect_stdout(fileobj, std_type='stdout'):
    oldstdout = getattr(sys, std_type)
    setattr(sys, std_type, fileobj)
    try:
        yield fileobj
    finally:
        setattr(sys, std_type, oldstdout)


redirect_stderr = partial(redirect_stdout, std_type='stderr')

with open('help_out.txt', 'w') as out, open('help_err.txt', 'w') as err:
    with redirect_stdout(out), redirect_stderr(err):
        msg = 'Test'
        sys.stdout.write('(stdout) A: {!r}\n'.format(msg))
        sys.stderr.write('(stderr) A: {!r}\n'.format(msg))
