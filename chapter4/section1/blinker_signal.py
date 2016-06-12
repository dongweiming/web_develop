# coding=utf-8
from blinker import signal

started = signal('test-started')


def each(round):
    print 'Round {}!'.format(round)


def round_two(round):
    print 'Only {}'.format(round)


started.connect(each)
started.connect(round_two, sender=2)

for round in range(1, 4):
    started.send(round)
