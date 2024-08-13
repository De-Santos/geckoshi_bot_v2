import logging
import threading

from rabbit import IReconnectingConsumer

logger = logging.getLogger(__name__)


def message_elevator_thread_launcher(consumer: IReconnectingConsumer) -> None:
    logging.info("start thread_consumer")

    def thread_target():
        try:
            consumer.run()
        except Exception as e:
            logger.error(f"Error in consumer thread: {e}")

    thread_consumer = threading.Thread(target=thread_target())
    thread_consumer.start()
