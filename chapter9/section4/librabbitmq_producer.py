# coding=utf-8
import sys

from librabbitmq import Connection

connection = Connection(host='localhost', userid='dongwm',
                        password='123456', virtual_host='web_develop')
channel = connection.channel()

channel.exchange_declare('web_develop', 'direct',
                         passive=False, durable=True, auto_delete=False)
if len(sys.argv) != 1:
    msg = sys.argv[1]
else:
    msg = 'hah'

channel.basic_publish(msg, 'web_develop', 'xxx_routing_key')

connection.close()
