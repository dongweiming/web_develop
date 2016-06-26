# coding=utf-8
import bz2
import glob
import collections
import itertools
import operator
import multiprocessing


class MapReduce(object):
    def __init__(self, map_func, reduce_func, num_workers=None):
        self.map_func = map_func  # map函数
        self.reduce_func = reduce_func  # reduce函数
        # num_workers为None表示默认可用cpu的核数
        self.pool = multiprocessing.Pool(num_workers)

    def partition(self, mapped_values):
        partitioned_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()

    def __call__(self, inputs, chunksize=1):
        # 其实MapReduce是通过multiprocessing.Pool.map这个函数实现, inputs是一个需要处理的列表
        # chunksize表示每次给mapper的量, 这个根据需求调整效率
        # 第一次是为了实现map把大任务分组, 最后获得全部分组的结果
        map_responses = self.pool.map(
            self.map_func, inputs, chunksize=chunksize)
        # chain把mapper的结果链接起来为一个可迭代的对象
        partitioned_data = self.partition(itertools.chain(*map_responses))
        # 第二次map是为了聚合结果实现reduce, map方法继续用来实现并行计算
        reduced_values = self.pool.map(self.reduce_func, partitioned_data)
        return reduced_values


def mapper_match(one_file):
    '''第一次的map函数,从每个文件里面获取符合的条目'''
    output = []
    for line in bz2.BZ2File(one_file).readlines():
        l = line.rstrip().split()
        if l[3] == 'web' and l[5] == '0':
            output.append((l[4], 1))
    # 返回格式类似 [(a, 1), (b, 3)] 这样的元组组成的列表
    return output


def reducer_match(item):
    '''第一次的reduce函数, 相同的key求合'''
    cookie, occurances = item
    return (cookie, sum(occurances))


def mapper_count(item):
    _, count = item  # 第二次map函数把符合的数量作为键
    return [(count, 1)]


def reducer_count(item):
    freq, occurances = item
    return (freq, sum(occurances))


if __name__ == '__main__':
    input_files = glob.glob(
        '/home/ubuntu/web_develop/chapter11/section1/data/*.bz2')
    mapper = MapReduce(mapper_match, reducer_match)
    cookie_feq = mapper(input_files)
    print 'Result: {}'.format(cookie_feq)
    mapper = MapReduce(mapper_count, reducer_count)
    cookie_feq = mapper(cookie_feq)
    cookie_feq.sort(key=operator.itemgetter(1), reverse=True)
    for freq, count in cookie_feq:
        print '{0}\t{1}'.format(freq, count)
