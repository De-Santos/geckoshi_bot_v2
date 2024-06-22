import asyncio
import logging

from confluent_kafka import Consumer
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

from kafka_processor import Topic


def on_assign(_, partitions):
    for partition in partitions:
        logging.info(f"Assigned partition: {partition.partition} for topic: {partition.topic}")


def poll_kafka_messages(consumer: Consumer, topic: str, queue: asyncio.Queue, loop):
    consumer.subscribe([topic], on_assign=on_assign)
    logging.info(f"Start listening topic: {topic}")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logging.error(f"ERROR: {msg.error()}")
            else:
                loop.call_soon_threadsafe(queue.put_nowait, msg)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        quit()


async def message_elevator(queue: asyncio.Queue, topic: Topic, c_type: type, func, loop):
    logging.info("Start message_elevator")
    protobuf_deserializer = ProtobufDeserializer(c_type, {'use.deprecated.format': False})
    while True:
        if queue.qsize() == 0:
            await asyncio.sleep(1)
            continue
        msg = queue.get_nowait()
        if msg is None:
            continue
        obj = protobuf_deserializer(msg.value(), SerializationContext(topic.value, MessageField.VALUE))
        logging.info(f"Consumed event from topic {msg.topic()}: key = {msg.key().decode('utf-8')}")
        loop.create_task(func(obj))
        queue.task_done()


def start_message_elevator_loop(queue: asyncio.Queue, topic: Topic, c_type: type, func, loop):
    lo = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    lo.run_until_complete(message_elevator(queue, topic, c_type, func, loop))
