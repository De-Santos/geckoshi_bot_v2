import datetime
import functools
import logging
import os
import traceback
from abc import abstractmethod, ABC
from asyncio import AbstractEventLoop

import pika
from pika.adapters.asyncio_connection import AsyncioConnection
from pika.channel import Channel

from database import get_session, get_mailing_message, MailingMessageStatus, MailingStatus, finish_mailing
from rabbit.classes import MessageDto
from variables import bot

logger = logging.getLogger(__name__)


class IReconnectingConsumer(ABC):
    @abstractmethod
    def run(self):
        pass


class MessageConsumer(object):
    from rabbit import Queue
    QUEUE = Queue.MESSAGE.value

    def __init__(self, url, loop, prefetch_count):

        self.should_reconnect = False
        self.was_consuming = False

        self._connection: AsyncioConnection | None = None
        self._channel: Channel | None = None
        self._url = url
        self._closing = False
        self._consumer_tag = None
        self._consuming = False
        self._outer_async_loop: AbstractEventLoop = loop
        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self._prefetch_count = prefetch_count

    def connect(self) -> AsyncioConnection:
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.adapters.asyncio_connection.AsyncioConnection

        """
        logger.info('Connecting to %s', self._url)
        return AsyncioConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
            custom_ioloop=self._outer_async_loop)

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            logger.info('Connection is closing or already closed')
        else:
            logger.info('Closing connection')
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :param pika.adapters.asyncio_connection.AsyncioConnection _unused_connection:
           The connection

        """
        logger.info('Connection opened')
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err: BaseException):
        """This method is called by pika if the connection to RabbitMQ
        can't be established.

        :param pika.adapters.asyncio_connection.AsyncioConnection _unused_connection: The connection
        :param Exception err: The error

        """
        logger.error('Connection open failed: %s', err)
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason: BaseException):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.adapters.asyncio_connection.AsyncioConnection _unused_connection: The closed connection obj
        :param Exception reason: exception representing reason for loss of connection.

        """
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            logger.warning('Connection closed, reconnect necessary: %s', reason)
            self.reconnect()

    def reconnect(self):
        """Will be invoked if the connection can't be opened or is
        closed. Indicates that a reconnect is necessary then stops the
        ioloop.

        """
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.

        """
        logger.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """
        logger.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        logger.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)
        self.setup_queue(self.QUEUE)

    def on_channel_closed(self, channel, reason):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shut down the object.

        :param pika.channel.Channel channel: The closed channel
        :param Exception reason: why the channel was closed

        """
        logger.warning('Channel %i was closed: %s', channel, reason)
        self.close_connection()

    def setup_queue(self, queue_name):
        """Set up the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        logger.info('Declaring queue %s', queue_name)
        cb = functools.partial(self.on_queue_declareok, userdata=queue_name)
        self._channel.queue_declare(queue=queue_name, callback=cb, durable=True)

    def on_queue_declareok(self, _unused_frame, userdata):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed.

        :param pika.frame.Method _unused_frame: The Queue.DeclareOk frame
        :param str|unicode userdata: Extra user data (queue name)

        """
        queue_name = userdata
        logger.info('Queue %s has been declared successfully', queue_name)
        self.set_qos()

    def set_qos(self):
        """This method sets up the consumer prefetch to only be delivered
        one message at a time. The consumer must acknowledge this message
        before RabbitMQ will deliver another one. You should experiment
        with different prefetch values to achieve desired performance.

        """
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        """Invoked by pika when the Basic.QoS method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method _unused_frame: The Basic.QosOk response frame

        """
        logger.info('QOS set to: %d', self._prefetch_count)
        self.start_consuming()

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        logger.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.QUEUE, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        logger.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        logger.info('Consumer was cancelled remotely, shutting down: %r',
                    method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        logger.info('Received message # %s from %s: %s', basic_deliver.delivery_tag, properties.app_id, body.decode())
        try:
            json_data = body.decode()
            logger.info(f"Decoded JSON: {json_data}")

            m = MessageDto.model_validate_json(json_data)
            self._outer_async_loop.create_task(self.__send_message(m, basic_deliver))
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            logger.debug(f"Stack trace: {traceback.format_exc()}")
            self.nack_message(basic_deliver.delivery_tag)

    async def __send_message(self, msg: MessageDto, basic_deliver) -> None:
        logger.info("Start message sending: %s", msg)
        s = get_session()
        mm = await get_mailing_message(msg.mailing_message_id, s=s)
        try:
            if mm.mailing.status != MailingStatus.CANCELED:
                await bot.send_message(chat_id=msg.destination_id,
                                       text=msg.message,
                                       reply_markup=msg.deserialize_button_markup())
                mm.status = MailingMessageStatus.COMPLETED
                logger.info(f"Message has been sent successfully: %s", msg)
            else:
                mm.status = MailingMessageStatus.CANCELED
                logger.info(f"Message has been canceled successfully: %s", msg)
            if msg.is_last:
                await finish_mailing(mm.mailing_id, s=s)
        except Exception as e:
            mm.status = MailingMessageStatus.FAILED
            mm.failed_message = str(e)
            logger.error(f"Failed to send message: {msg} with error: {e}")
            logger.debug(f"Stack trace: {traceback.format_exc()}")
        finally:
            mm.sent_at = datetime.datetime.now(datetime.UTC)
            await s.commit()
            await s.close()
            self.ack_message(basic_deliver.delivery_tag)

    def ack_message(self, delivery_tag):
        logger.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def nack_message(self, delivery_tag):
        logger.info('Nack message %s', delivery_tag)
        self._channel.basic_nack(delivery_tag)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        if self._channel:
            logger.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method _unused_frame: The Basic.CancelOk frame
        :param str|unicode userdata: Extra user data (consumer tag)

        """
        self._consuming = False
        logger.info('RabbitMQ acknowledged the cancellation of the consumer: %s', userdata)
        self.close_channel()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        logger.info('Closing the channel')
        self._channel.close()

    def run(self):
        self._connection = self.connect()
        # self._connection.ioloop.run_forever()

    def stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.

        """
        if not self._closing:
            self._closing = True
            logger.info('Stopping')
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.run_forever()
            else:
                self._connection.ioloop.stop()
            logger.info('Stopped')


class MessageConsumerRunner:

    def __init__(self, loop):
        self._reconnect_delay = 0
        self._amqp_url = os.getenv("RABBIT_URL")
        self._prefetch_count = int(os.getenv("RABBIT_PREFETCH_COUNT"))
        self._loop = loop
        self._consumer = MessageConsumer(self._amqp_url, self._loop, self._prefetch_count)

    def run(self):
        try:
            self._consumer.run()
        except KeyboardInterrupt:
            self._consumer.stop()
