# coding=utf-8
from MySQLdb import IntegrityError

from stubs import cache, store, mc_delete


class MovieOrder(object):
    MC_KEY = 'chapter15:section2:movie_roder:%s'

    def __init__(self, id, type_id, order_id, price):
        self.id = id
        self.type_id = type_id
        self.price = price

    @classmethod
    @cache(MC_KEY % '{id}')
    def get(cls, id):
        sql = ('select id, type_id, order_id, price from movie_order '
               'where id=%s')
        rs = store.execute(sql, id)
        return cls(*rs[0]) if rs else ''

    @classmethod
    def delete(cls, id):
        sql = 'delete from movie_order where id=%s'
        try:
            store.execute(sql, id)
            store.commit()
        except IntegrityError:
            store.rollback()
            return False

        cls.clear_mc(id)
        return True

    def update_price(self, price):
        sql = 'update movie_order set price=%s where id=%s'
        updated = store.execute(sql, (price, self.id))
        if updated:
            store.commit()
            mc_delete(self.MC_KEY % self.id)
        return updated

    @classmethod
    def clear_mc(cls, id):
        mc_delete(cls.MC_KEY % id)
