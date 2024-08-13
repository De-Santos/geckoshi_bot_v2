import asyncio
import logging
import os
import time
import uuid
from typing import List

import pika
from pika.adapters.blocking_connection import BlockingConnection
from pika.delivery_mode import DeliveryMode
from pika.exceptions import AMQPConnectionError, AMQPError
from pika.spec import BasicProperties
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class BlockingTransactionalPublisher:
    def __init__(self, queue_name: str, retry_attempts=5, base_retry_delay=1.0):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.retry_attempts = retry_attempts
        self.base_retry_delay = base_retry_delay
        self.loop = asyncio.get_event_loop()
        self.c_uid = uuid.uuid4()

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def _connect(self):

        connected = False
        attempt = 0
        while not connected and attempt < self.retry_attempts:
            try:
                self.connection = BlockingConnection(pika.URLParameters(os.getenv("RABBIT_URL")))
                self.channel = self.connection.channel()
                connected = True
            except AMQPConnectionError as e:
                logger.warning(f"CLASS_UID: [{self.c_uid}] - Connection attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(self.base_retry_delay * 2 ** attempt)
                attempt += 1

        if not connected:
            raise AMQPConnectionError(f"CLASS_UID: [{self.c_uid}] - Failed to connect after multiple attempts")

    async def publish_messages(self, messages: List["BaseModel"]) -> bool:
        if not self.channel:
            await self._connect()

        uid = uuid.uuid4()
        start_time = time.perf_counter()  # Start time tracking
        logger.info("UID: [%s] - Start sending batch[%s] of messages.", uid, len(messages))

        try:
            await self.loop.run_in_executor(None, lambda: self.channel.tx_select())
            for message in messages:
                await self.loop.run_in_executor(None, lambda: self.channel.basic_publish(
                    exchange='',
                    routing_key=self.queue_name,
                    body=message.model_dump_json(),
                    properties=BasicProperties(
                        content_type='application/json',
                        delivery_mode=DeliveryMode.Persistent
                    )
                ))
            await self.loop.run_in_executor(None, lambda: self.channel.tx_commit())

            elapsed_time = time.perf_counter() - start_time  # Calculate elapsed time
            logger.info("CLASS_UID: [%s] UID: [%s] - All messages published successfully. Transaction took %.2f seconds.", self.c_uid, uid, elapsed_time)
            return True
        except AMQPError as e:
            await self.loop.run_in_executor(None, lambda: self.channel.tx_rollback())
            elapsed_time = time.perf_counter() - start_time  # Calculate elapsed time
            logger.error("CLASS_UID: [%s] UID: [%s] - Publishing failed, rolled back the transaction. Error: %s. Transaction took %.2f seconds.", self.c_uid, uid, e, elapsed_time)
            return False

    async def close(self):
        if self.connection and self.connection.is_open:
            await self.loop.run_in_executor(None, lambda: self.connection.close())
