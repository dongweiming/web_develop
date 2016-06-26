# coding=utf-8
import os
import glob
import collections
from functools import wraps
import itertools

from dpark import DparkContext


def exclude_unusual(f):
    @wraps(f)
    def wrapper(log, *a, **kw):
        if int(log.access_type) < 3 and int(log.statue_code) < 400:
            return f(log, *a, **kw)
        return []
    return wrapper


_Weblog = collections.namedtuple('Weblog', [
    'date', 'time', 'uid', 'url', 'browser_type', 'statue_code',
    'encrypted_ip', 'url_referer', 'access_type']
)


class Weblog(_Weblog):
    @classmethod
    def from_line(cls, line):
        fields = line.strip().split('\t')
        return cls(*fields)


class BaseRunner(object):
    def __init__(self, log_path=None, date_=None, match_rules=None):
        if log_path is None:
            log_path = '/mfs/log/web_log'
        self.date = [] if date_ is None else date_
        # match_rules 来定义多个 {'uv': filter_func}
        self.match_rules = {} if match_rules is None else match_rules

    def _filter_func(self):
        filter_func_list = self.match_rules.values()

        def wrapper(log, *args, **kwargs):
            return any(func(log, *args, **kwargs)
                       for func in filter_func_list)

        return wrapper

    def _get_paths_by_date(self, date_):
        return glob.glob(os.path.join(
            self.log_path, '*', '*', '*', 'fact_web_log.gz',
            date_.strftime('%Y%m%d')
        ))

    @property
    def paths(self):
        return itertools.chain(self._get_paths_by_date(date_)
                               for date_ in self.date)

    def get_rdd(self):
        dpark = DparkContext()

        return dpark.union(
            [dpark.textFile(path, splitSize=64 << 20)
             for path in self.paths]
        ).map(Weblog.from_line)

    def get_flat_mapped_rdd(self):
        filter_func = self._filter_func()
        map_func = self._map_func()
        return (self.get_rdd()
                .filter(filter_func)
                .map(map_func)
                .flatMap(lambda x: x))

    def get_result(self):
        raise NotImplementedError


class PVRunner(BaseRunner):

    def _map_func(self):
        def wrapper(log, *args, **kw):
            values = []
            for k, v in self.match_rules.iteritems():
                if v(log, *args, **kw):
                    values.append((k, 1))
            return values
        return wrapper

    def get_result(self):
        flat_mapped_rdd = self.get_flat_mapped_rdd()
        return (flat_mapped_rdd.reduceByKey(lambda x, y: x + y)
                .collectAsMap())


class UVRunner(BaseRunner):
    def _map_func(self):
        def wrapper(log, *args, **kw):
            values = []
            for k, v in self.match_rules.iteritems():
                if v(log, *args, **kw):
                    values.append((k, log.uid, 1))
            return values
        return wrapper

    def get_result(self):
        flat_mapped_rdd = self.get_flat_mapped_rdd()
        return (flat_mapped_rdd.uniq()
                .map(lambda x: (x[0], 1))
                .reduceByKey(lambda x, y: x + y)
                .collectAsMap())
