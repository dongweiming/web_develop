# coding=utf-8
from kombu import Connection, Exchange, Queue, Consumer
from kombu.async import Hub

web_exchange = Exchange('web_develop', 'direct', durable=True)
standard_queue = Queue('standard', exchange=web_exchange,
                       routing_key='web.develop')

URI = 'librabbitmq://dongwm:123456@localhost:5672/web_develop'
hub = Hub()


def on_message(body, message):
    print("Body:'%s', Headers:'%s', Payload:'%s'" % (
        body, message.content_encoding, message.payload))
    message.ack()


with Connection(URI) as connection:
    connection.register_with_event_loop(hub)
    with Consumer(connection, standard_queue, callbacks=[on_message]):
        try:
            hub.run_forever()
        except KeyboardInterrupt:
            exit(1)
