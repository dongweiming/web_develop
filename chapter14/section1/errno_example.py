# coding=utf-8
import os
import errno


def listdir(dirname):
    try:
        os.listdir(dirname)
    except OSError as e:
        error = e.errno
        if error == errno.ENOENT:
            print 'No such file or directory'
        elif error == errno.EACCES:
            print 'Prmission denied'
        elif error == errno.ENOSPC:
            print 'No space left on device'
        else:
            print e.strerror
    else:
        print 'No error!'


for filename in ['/no/such/dir', '/root', '/home/vagrant']:
    listdir(filename)
