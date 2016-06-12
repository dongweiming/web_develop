# coding=utf-8
from functools import partial


class partialmethod(partial):  # noqa
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return partial(self.func, instance,
                       *(self.args or ()), **(self.keywords or {}))


def get_name(self):
    return self._name


class Cell(object):
    def __init__(self, name):
        self._alive = False
        self._name = name

    @property
    def alive(self):
        return self._alive

    def set_state(self, state):
        self._alive = bool(state)
    set_alive = partialmethod(set_state, True)
    set_dead = partialmethod(set_state, False)

    get_name = partialmethod(get_name)


cell = Cell('cell_1')
print cell.alive
cell.set_alive()
print cell.alive
print cell.get_name()
