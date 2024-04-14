import json
import pika
import redis
import os
from dotmap import DotMap
import functools
import time
import sys
import sentry_sdk

sentry_sdk.init(
    dsn="https://40425deb8455f665b472e012d073c7f1@o127869.ingest.sentry.io/4506388932067328",
    traces_sample_rate=0.0,
)
redis_connection = redis.from_url("redis://redis:6379/0")

def on_message(channel, method_frame, header_frame, body, ball):
    message = json.loads(body)
    print('megalith zpool status', message['zpool_status'])
    message['timestamp'] = int(time.time())
    if message['synced_to_chain'] == True:
        message['last_confirmed_synced_to_chain'] = int(time.time())
    redis_key = "megalith-status"
    redis_connection.set(redis_key, json.dumps(message))
    print('wrote megalith status')
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

def get_messages_from_rabbitmq(ball):
    try:
        on_message_callback = functools.partial(on_message, ball=ball)
        consumer_tag = 'ln-helper'
        print("rabbit consumer starting")
        ball.channel.basic_consume(
            "ln-megalith-status", on_message_callback, consumer_tag=consumer_tag
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
    print("---starting listen to megalith----")
    ball = DotMap()
    rabbit_url = os.getenv("RABBITMQ_URL", "unk-url")
    params = pika.URLParameters(rabbit_url + "?heartbeat=500")
    connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    ball.channel = channel

    while True:
        get_messages_from_rabbitmq(ball)

start_listening()