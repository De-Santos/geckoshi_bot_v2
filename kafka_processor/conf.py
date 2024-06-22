import os
from enum import Enum

from confluent_kafka import Producer, Consumer
from dotenv import load_dotenv

load_dotenv()


class Topic(Enum):
    TRANSACTION = "transactions"
    MESSAGE = "message"


producer_config = {
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
    'sasl.username': os.getenv('SASL_USERNAME'),
    'sasl.password': os.getenv('SASL_PASSWORD'),

    # Fixed properties
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'acks': 'all'
}
consumer_config = {
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
    'sasl.username': os.getenv('SASL_USERNAME'),
    'sasl.password': os.getenv('SASL_PASSWORD'),

    # Fixed properties
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'group.id': 'kafka-geckoshi_consumer',
    'auto.offset.reset': 'earliest'
}
