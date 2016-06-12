# coding=utf-8
import shutil
from os import path

from jinja2 import Environment, DictLoader, BytecodeCache


class MyCache(BytecodeCache):

    def __init__(self, directory):
        self.directory = directory

    def load_bytecode(self, bucket):
        filename = path.join(self.directory, bucket.key)
        if path.exists(filename):
            with open(filename, 'rb') as f:
                bucket.load_bytecode(f)

    def dump_bytecode(self, bucket):
        filename = path.join(self.directory, bucket.key)
        with open(filename, 'wb') as f:
            bucket.write_bytecode(f)

    def clear(self):
        shutil.rmtree(self.directory)


if __name__ == '__main__':
    loader = DictLoader({'hello.html': 'Hello {{ name }}'})
    env = Environment(loader=loader, bytecode_cache=MyCache('/tmp'))
    template = env.get_template('hello.html')
    print template.render(name='Xiao Ming')
