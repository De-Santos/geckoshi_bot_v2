import asyncio
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

from kafka_processor import Topic, register_consumer
from kafka_processor.consumer import poll_kafka_messages, start_message_elevator_loop


def message_elevator_thread_launcher(loop, topic: Topic, c_type: type, message_observer) -> None:
    queue = asyncio.Queue()
    consumer = register_consumer()
    logging.info("start thread_consumer")
    thread_consumer = threading.Thread(target=poll_kafka_messages, args=(consumer, topic.value, queue, loop))
    thread_consumer.start()

    logging.info("start executor for start_message_elevator_loop")
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(start_message_elevator_loop, queue, topic, c_type, message_observer, loop)

