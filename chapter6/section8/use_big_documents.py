# coding=utf-8
import random
from datetime import datetime, timedelta

import pymongo

RANGE = 1440
l = [random.randint(1, 100) for i in range(RANGE)]  # 模拟一天的数据
client = pymongo.MongoClient("localhost", 27017)
client.drop_database('test')  # 保证之前没有数据
db = client.test

# 传统方案
for i in range(RANGE):
    s = {'metric': 'review_count', 'client_type': 2, 'value': l[i],
         'date': datetime(2016, 03, 22, 0, 0) + timedelta(minutes=i)}
    db.a.insert_one(s)


# 但是单个大文档(每小时一个文档)
for i in range(24):
    s = {'metric': 'review_count', 'client_type': 2,
         'date': '2016-03-22', 'hour': i}
    s.update({str(k): v for k, v in enumerate(l[60 * i:60 * (i + 1)])})
    db.b.insert_one(s)


def get_hour_data1(hour):
    return [i['value'] for i in db.a.find({
        'date': {'$gte': datetime(2016, 3, 22, hour, 0),
                 '$lt': datetime(2016, 3, 22, hour + 1, 0)}})]


def get_hour_data2(hour):
    c = db.b.find_one({'hour': hour})
    return [c[str(i)] for i in range(60)]
