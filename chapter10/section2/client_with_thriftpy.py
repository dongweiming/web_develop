# coding=utf-8
import os

import thriftpy
from thriftpy.rpc import client_context
from thriftpy.protocol import TBinaryProtocolFactory
from thriftpy.transport import TBufferedTransportFactory

HERE = os.path.abspath(os.path.dirname(__file__))

calc_thrift = thriftpy.load(
    os.path.join(HERE, 'calc.thrift'),
    module_name='calc_thrift')

with client_context(calc_thrift.CalcService,
                    '127.0.0.1', 8300,
                    proto_factory=TBinaryProtocolFactory(),
                    trans_factory=TBufferedTransportFactory(),
                    timeout=None) as calc:
    rs = calc.add(1, 2)
    print 'Result is: {}'.format(rs)
