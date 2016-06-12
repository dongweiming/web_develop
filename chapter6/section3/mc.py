# coding=utf-8
from libmc import (
    Client, MC_HASH_MD5, MC_POLL_TIMEOUT, MC_CONNECT_TIMEOUT, MC_RETRY_TIMEOUT
)
from mc_decorator import create_decorators

mc = Client(
    [
        'localhost',
        'localhost:11212',
        'localhost:11213 mc_213'
    ],
    do_split=True,
    comp_threshold=0,
    noreply=False,
    prefix=None,
    hash_fn=MC_HASH_MD5,
    failover=False
)

mc.config(MC_POLL_TIMEOUT, 100)  # 100 ms
mc.config(MC_CONNECT_TIMEOUT, 300)  # 300 ms
mc.config(MC_RETRY_TIMEOUT, 5)  # 5 s

globals().update(create_decorators(mc))
