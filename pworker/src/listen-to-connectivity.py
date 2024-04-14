import json
import pika
import redis
import os
from dotmap import DotMap
import functools
import time
import sys
redis_connection = redis.from_url("redis://redis:6379/0")

def on_message(channel, method_frame, header_frame, body, ball):
    message = json.loads(body)
    message['timestamp'] = int(time.time())
    redis_key = "connectivity-status"
    redis_connection.set(redis_key, json.dumps(message))
    print('wrote connectivity status')
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

def get_messages_from_rabbitmq(ball):
    try:
        on_message_callback = functools.partial(on_message, ball=ball)
        print("rabbit consumer starting")
        ball.channel.basic_consume(
            "megalith-docs-connectivity", on_message_callback,
        )
        try:
            ball.channel.start_consuming()
        except KeyboardInterrupt:
            ball.channel.stop_consuming()
            ball.connection.close()
            sys.exit()
    except pika.exceptions.AMQPConnectionError as e:
        print(e)

def start_listening():
    print("---starting listen to connectivity----")
    ball = DotMap()
    rabbit_url = os.getenv("RABBITMQ_URL", "unk-url")
    params = pika.URLParameters(rabbit_url + "?heartbeat=500")
    connection = pika.BlockingConnection(params) 
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    ball.channel = channel

    while True:
        get_messages_from_rabbitmq(ball)

start_listening()