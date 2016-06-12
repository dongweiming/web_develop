# coding=utf-8
import redis
from mako.cache import CacheImpl, register_plugin as _register_plugin

_redis_cache = None


class RedisCacheImpl(CacheImpl):
    def __init__(self, cache):
        global _redis_cache
        if _redis_cache is None:
            _redis_cache = redis.StrictRedis.from_url(
                cache.template.cache_args['url'])
        super(RedisCacheImpl, self).__init__(_redis_cache)

    def get_or_create(self, key, creation_function, **kw):
        value = self.get(key)
        if value is None:
            value = creation_function()
            self.set(key, value)
        return value

    def set(self, key, value, **kwargs):
        self.cache.set(key, value)

    def get(self, key, **kwargs):
        return self.cache.get(key)

    def invalidate(self, key, **kwargs):
        return self.cache.delete(key)


def register_plugin():
    # optional - register the class locally
    _register_plugin("redis", __name__, "RedisCacheImpl")
