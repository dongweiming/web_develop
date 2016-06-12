# coding=utf-8

auto_builtins = ['edit', 'cd', 'mv', 'cp', 'rm', 'rmdir', 'execfile',
                 'pwd', 'pushd', 'popd', 'env', 'mkdir', 'eval', 'exec',
                 'run', 'pdoc', 'ed', 'env', 'cat', 'cpaste', 'less',
                 'more', 'paste', 'save', 'system', 'sx'
                 ]

disable_attributes = {
    'os': [
        'system', 'mkdir', 'rmdir', 'chdir', 'remove', 'removedirs',
        'rename', 'renames', 'chroot', 'popen', 'popen2', 'popen3',
        'popen4'
    ],
    'subprocess': [
        'Popen', 'call', 'check_call'
    ],
    'multiprocessing': [
        'Process', 'Pool', 'process'
    ],
}


from IPython import get_ipython


class HideAttribute(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args):
        return 'This feature is disabled'

# Disable some convenience functions to __builtin__
import __builtin__
ip = get_ipython()
disable = HideAttribute()
realimp = __builtin__.__import__
line = ip.magics_manager.magics['line']
# Disable ipython system shell
ip.system = disable

# Disable function to __builtin__
for n in auto_builtins:
    __builtin__.__dict__[n] = disable


# Disable all magic in ipython
for k in line.keys():
    if k not in ['connect_info', 'debug']:
        line[k] = disable


def limited_import(name, globals={}, locals={}, fromlist=[], level=-1):
    importer = realimp(name, globals, locals, fromlist, level)
    if name in disable_attributes:
        for a in disable_attributes[name]:
            if hasattr(importer, a):
                setattr(importer, a, disable)
    return importer

__builtin__.__import__ = limited_import
