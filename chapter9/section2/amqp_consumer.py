# coding=utf-8
import pika


# 处理接收到的消息的回调函数
# method_frame携带了投递标记， header_frame表示AMQP信息头的对象
# body为消息实体
def on_message(channel, method_frame, header_frame, body):
    # 消息确认， 确认之后才会删除消息并给消费者发送新的消息
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    print body

parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='web_develop', exchange_type='direct',
                         passive=False, durable=True, auto_delete=False)
# 声明队列， 如果没有就创建
channel.queue_declare(queue='standard', auto_delete=True)
# 通过路由键将队列和交换机绑定
channel.queue_bind(queue='standard', exchange='web_develop',
                   routing_key='xxx_routing_key')

channel.basic_consume(on_message, 'standard')  # 订阅队列

try:
    channel.start_consuming()  # 开始消费
except KeyboardInterrupt:
    channel.stop_consuming()  # 退出消费

connection.close()
