import os

import pika
from dotenv import load_dotenv

load_dotenv()

message_exchange: str = 'message-exc'

message_queue_name: str = os.getenv("RABBIT_MESSAGE_QUEUE")

parameters = pika.URLParameters(os.getenv("RABBIT_URL"))
connection = pika.BlockingConnection(parameters=parameters)

channel = connection.channel()

channel.exchange_declare(exchange=message_exchange, exchange_type='direct')

channel.queue_declare(queue=message_queue_name)

channel.queue_bind(exchange=message_exchange, queue=message_queue_name)

