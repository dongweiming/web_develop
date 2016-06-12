# coding=utf-8
import sys
from datetime import datetime

from supervisor import childutils


def write_log(headers, payload):
    if not headers['eventname'].startswith('PROCESS_STATE_'):
        return
    f = open('/tmp/log.txt', 'a')
    f.write(str(headers) + '\n\n')
    pheaders, pdata = childutils.eventdata(payload + '\n')

    pheaders['dt'] = datetime.now()

    msg = ('[{dt}]Process {processname} in group {groupname} exited '
           'unexpectedly (pid {pid}) from state {from_state}\n').format(
        **pheaders)
    f.write(msg)
    f.flush()
    f.close()


def main():
    while 1:
        headers, payload = childutils.listener.wait(sys.stdin, sys.stdout)
        write_log(headers, payload)
        childutils.listener.ok(sys.stdout)


if __name__ == '__main__':
    main()
