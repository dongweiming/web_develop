# coding=utf-8
import random

import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
client.drop_database('test')  # 保证之前没有数据， 删除名为test的数据库
db = client.test  # 使用test这个数据库
coll = db.coll  # 使用coll这个集合

# 插入单条
rs = coll.insert_one({'a': 1, 'b': 2})
object_id = rs.inserted_id
print rs.inserted_id  # 打印插入的对象id

# 插入多条
rs = coll.insert_many([{'a': random.randint(1, 10), 'b': 10}
                       for _ in range(10)])

print rs.inserted_ids  # 打印插入的对象id列表

# 查询单条（符合的第一条）
print coll.find_one({'a': 1, 'b': 2})

# 集合当前全部文档数
print coll.count()

cursor = coll.find({'a': {'$lte': 1}})  # 查询结果是一个游标
print cursor.count()  # 符合查询的文档数

for r in cursor:
    print r, r['b']  # 打印符合查询的文档内容， 以及其中b键的值

# 注意， 这个循环只能进行一次. 如果想再获得需要重新find或者使用list(cursor)把结果存起来

# 对查询结果排序
print list(coll.find({'a': {'$lte': 1}}).sort([('b', -1)]))
# -1也可以表示为pymongo.DESCENDING

# 对查询结果可以限制返回文档数， 控制跳过的结果数
print coll.find({'b': {'$gt': 1}}).limit(1).skip(1).next()  # next相当于find_one

# 找到后更新， 下面例子第一个参数是过滤条件， 第二个参数是要更新的操作（设置b为3， a自增长1）
# upsert为True表示找不到会创建一个,也就是get_or_create
rs = coll.find_one_and_update({'a': 1, 'b': 2},
                              {'$set': {'b': 3}, '$inc': {'a': 1}},
                              upsert=False)
print rs  # 返回更新前的文档
# 同样的还有find_one_and_replace和find_one_and_delete
print list(coll.find({'a': 2, 'b': 3}))  # 上述文档已经被更新为这个文档
coll.find_one_and_update({'a': 1, 'b': 2},
                         {'$set': {'b': 3}, '$inc': {'a': 1}},
                         upsert=True)  # 虽然没有符合{'a': 1, 'b': 2}的记录，但是会新建一个
print coll.find({'a': 2, 'b': 3}).count()  # 发现现在有2条文档记录了


# 删除单个文档
coll.delete_one({'a': 2, 'b': 3})

# 一次性删除多个文档

rs = coll.delete_many({'a': 2, 'b': 3})
# 如果没有符合的条目也不会提示， 但是可以通过rs.deleted_count获得删除的数量
print rs.deleted_count
