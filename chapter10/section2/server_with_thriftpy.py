# coding=utf-8
import os
import logging

import thriftpy
from thriftpy.rpc import make_server
from thriftpy.protocol import TBinaryProtocolFactory
from thriftpy.transport import TBufferedTransportFactory

HERE = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig()

calc_thrift = thriftpy.load(
    os.path.join(HERE, 'calc.thrift'),
    module_name='calc_thrift')


class Dispatcher(object):
    def add(self, a, b):
        return a + b


server = make_server(calc_thrift.CalcService,
                     Dispatcher(),
                     '127.0.0.1', 8300,
                     proto_factory=TBinaryProtocolFactory(),
                     trans_factory=TBufferedTransportFactory())
print 'serving...'
server.serve()
