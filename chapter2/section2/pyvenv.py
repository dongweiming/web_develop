import os
import sys
import argparse
import venv
from subprocess import Popen, PIPE
from threading import Thread
from urllib.parse import urlparse
from urllib.request import urlretrieve

PYPI_URL = 'https://pypi.python.org/packages/source/'


class ExtendedEnvBuilder(venv.EnvBuilder):

    def __init__(self, *args, **kwargs):
        self.nodist = kwargs.pop('nodist', False)
        self.nopip = kwargs.pop('nopip', False)
        self.progress = kwargs.pop('progress', None)
        self.verbose = kwargs.pop('verbose', False)
        self.reqs = kwargs.pop('reqs', [])
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        os.environ['VIRTUAL_ENV'] = context.env_dir
        for req in self.reqs:
            self.install_req(context, req)

    def create(self, env_dir):
        super().create(env_dir)
        if not env_dir.startswith('/'):
            env_dir = os.path.join(os.getcwd(), env_dir)
        print('Installed {}'.format(env_dir))

    def reader(self, stream, context):
        progress = self.progress
        while True:
            s = stream.readline()
            if not s:
                break
            if progress is not None:
                progress(s, context)
            else:
                if not self.verbose:
                    sys.stderr.write('.')
                else:
                    sys.stderr.write(s.decode('utf-8'))
                sys.stderr.flush()
        stream.close()

    def install_script(self, context, name, args, distpath=None):
        progress = self.progress
        binpath = context.bin_path

        if self.verbose:
            term = '\n'
        else:
            term = ''
        if progress is not None:
            progress('Installing %s ...%s' % (name, term), 'main')
        else:
            sys.stderr.write('Installing %s ...%s' % (name, term))
            sys.stderr.flush()

        p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=binpath)
        t1 = Thread(target=self.reader, args=(p.stdout, 'stdout'))
        t1.start()
        t2 = Thread(target=self.reader, args=(p.stderr, 'stderr'))
        t2.start()
        p.wait()
        t1.join()
        t2.join()
        if progress is not None:
            progress('done.', 'main')
        else:
            sys.stderr.write('done.\n')
        if distpath is not None:
            os.unlink(distpath)

    def install_req(self, context, req):
        args = [os.path.join(context.bin_path, 'pip'), 'install', req]
        self.install_script(context, req, args)


def main(args=None):
    compatible = True
    if sys.version_info < (3, 3):
        compatible = False
    elif not hasattr(sys, 'base_prefix'):
        compatible = False
    if not compatible:
        raise ValueError('This script is only for use with '
                         'Python 3.3 or later')

    parser = argparse.ArgumentParser(
        prog=__name__, description=(
            'Creates virtual Python environments in one or '
            'more target directories.'))
    parser.add_argument('dirs', metavar='ENV_DIR', nargs='+',
                        help='A directory to create the environment in.')
    parser.add_argument('-r', '--req', nargs='*',
                        dest='reqs', help=(
                            'specify additional required distributions'))
    if os.name == 'nt':
        use_symlinks = False
    else:
        use_symlinks = True
    parser.add_argument('--symlinks', default=use_symlinks,
                        action='store_true', dest='symlinks',
                        help='Try to use symlinks rather than copies, '
                        'when symlinks are not the default for '
                        'the platform.')
    parser.add_argument('--clear', default=False, action='store_true',
                        dest='clear', help=(
                            'Delete the contents of the '
                            'environment directory if it '
                            'already exists, before '
                            'environment creation.'))
    parser.add_argument('--upgrade', default=False, action='store_true',
                        dest='upgrade', help=(
                            'Upgrade the environment '
                            'directory to use this version '
                            'of Python, assuming Python '
                            'has been upgraded in-place.'))
    options = parser.parse_args(args)
    if options.upgrade and options.clear:
        raise ValueError(
            'you cannot supply --upgrade and --clear together.')
    builder = ExtendedEnvBuilder(
        clear=options.clear, symlinks=options.symlinks,
        upgrade=options.upgrade,
        reqs=options.reqs, with_pip=True)
    for d in options.dirs:
        builder.create(d)


if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)
