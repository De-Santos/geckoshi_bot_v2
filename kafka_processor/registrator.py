from confluent_kafka import Consumer, Producer

from kafka_processor import producer_config, consumer_config


def register_producer() -> Producer:
    p = Producer(producer_config)
    return p


def register_consumer() -> Consumer:
    return Consumer(consumer_config)
