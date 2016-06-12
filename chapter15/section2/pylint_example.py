# coding=utf-8
import os
import sys

from pylint import lint


if len(sys.argv) > 1:
    FILES = sys.argv[1:]
else:
    FILES = []
    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        FILES.extend(
            os.path.join(dirpath, filename)
            for filename in filenames
            if filename.endswith('.py')
        )

MESSAGES = ['C0202', 'E0102', 'E0211', 'E0213', 'E1120', 'E1121',
            'E1123', 'W0613', 'R0401', 'R0801']

args = [
    '--reports=n',
    '--disable=all',
    '--msg-template="{path}:{line}: [{msg_id}, {obj}] {msg}"',
    '--enable={}'.format(','.join(MESSAGES))
]

args.extend(FILES)

if __name__ == '__main__':
    sys.exit(lint.Run(args))
