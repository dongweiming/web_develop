# coding=utf-8
import sys

import pika

# %2F是被转义的/， 这里使用了默认的虚拟主机、 默认的guest这个账号和密码
parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
connection = pika.BlockingConnection(parameters)  # connection就是所谓的消息代理
channel = connection.channel()  # 获得信道

# 声明交换机，指定交换类型为直接交换。 最后2个参数表示想要持久化的交换机
channel.exchange_declare(exchange='web_develop', exchange_type='direct',
                         passive=False, durable=True, auto_delete=False)
if len(sys.argv) != 1:
    msg = sys.argv[1]  # 使用命令行参数作为消息体
else:
    msg = 'hah'

# 创建一个消息， delivery_mode为2表示让这个消息持久化， 重启RabbitMQ也不会丢失
props = pika.BasicProperties(content_type='text/plain', delivery_mode=2)
# basic_publish表示发送路由键为xxx_routing_key，消息体为haha的消息给web_develop这个交换机
channel.basic_publish('web_develop', 'xxx_routing_key', msg,
                      properties=props)
connection.close()  # 关闭连接
