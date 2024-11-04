import datetime
import functools
import logging
import traceback
from abc import abstractmethod, ABC
from asyncio import AbstractEventLoop

import pika
from pika.adapters.asyncio_connection import AsyncioConnection
from pika.channel import Channel

import cheque
from database import get_session, get_mailing_message, MailingMessageStatus, MailingStatus, finish_mailing, get_cheque_activation, ChequeActivationStatus, TransactionOperation, now
from rabbit.classes import MessageDto, ActivationPersonalChequeDto
from transaction_manager import make_transaction_from_system, generate_trace, TraceType
from variables import bot


class IReconnectingConsumer(ABC):
    @abstractmethod
    def run(self):
        pass


class MessageConsumer(object):
    from rabbit import Queue
    QUEUE = Queue.MESSAGE.value

    def __init__(self, url, loop, prefetch_count):
        self.logger = logging.getLogger(__class__.__name__)

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
        self.logger.info('Connecting to %s', self._url)
        return AsyncioConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
            custom_ioloop=self._outer_async_loop)

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            self.logger.info('Connection is closing or already closed')
        else:
            self.logger.info('Closing connection')
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :param pika.adapters.asyncio_connection.AsyncioConnection _unused_connection:
           The connection

        """
        self.logger.info('Connection opened')
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err: BaseException):
        """This method is called by pika if the connection to RabbitMQ
        can't be established.

        :param pika.adapters.asyncio_connection.AsyncioConnection _unused_connection: The connection
        :param Exception err: The error

        """
        self.logger.error('Connection open failed: %s', err)
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
            self.logger.warning('Connection closed, reconnect necessary: %s', reason)
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
        self.logger.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """
        self.logger.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        self.logger.info('Adding channel close callback')
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
        self.logger.warning('Channel %i was closed: %s', channel, reason)
        self.close_connection()

    def setup_queue(self, queue_name):
        """Set up the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        self.logger.info('Declaring queue %s', queue_name)
        cb = functools.partial(self.on_queue_declareok, userdata=queue_name)
        self._channel.queue_declare(queue=queue_name, callback=cb, durable=True)

    def on_queue_declareok(self, _unused_frame, userdata):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed.

        :param pika.frame.Method _unused_frame: The Queue.DeclareOk frame
        :param str|unicode userdata: Extra user data (queue name)

        """
        queue_name = userdata
        self.logger.info('Queue %s has been declared successfully', queue_name)
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
        self.logger.info('QOS set to: %d', self._prefetch_count)
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
        self.logger.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.QUEUE, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        self.logger.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        self.logger.info('Consumer was cancelled remotely, shutting down: %r',
                         method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        self.logger.info('Received message # %s from %s: %s', basic_deliver.delivery_tag, properties.app_id, body.decode())
        try:
            json_data = body.decode()
            self.logger.info(f"Decoded JSON: {json_data}")

            m = MessageDto.model_validate_json(json_data)
            self._outer_async_loop.create_task(self.__send_message(m, basic_deliver))
        except Exception as e:
            self.logger.error(f"Failed to process message: {e}")
            self.logger.debug(f"Stack trace: {traceback.format_exc()}")
            self.nack_message(basic_deliver.delivery_tag)

    async def __send_message(self, msg: MessageDto, basic_deliver) -> None:
        self.logger.info("Start message sending: %s", msg)
        s = get_session()
        mm = await get_mailing_message(msg.mailing_message_id, s=s)
        try:
            if mm.mailing.status != MailingStatus.CANCELED:
                await bot.send_message(chat_id=msg.destination_id,
                                       text=msg.message,
                                       reply_markup=msg.deserialize_button_markup())
                mm.status = MailingMessageStatus.COMPLETED
                self.logger.info(f"Message has been sent successfully: %s", msg)
            else:
                mm.status = MailingMessageStatus.CANCELED
                self.logger.info(f"Message has been canceled successfully: %s", msg)
            if msg.is_last:
                await finish_mailing(mm.mailing_id, s=s)
        except Exception as e:
            mm.status = MailingMessageStatus.FAILED
            mm.failed_message = str(e)
            self.logger.error(f"Failed to send message: {msg} with error: {e}")
            self.logger.debug(f"Stack trace: {traceback.format_exc()}")
        finally:
            mm.sent_at = datetime.datetime.now(datetime.UTC)
            await s.commit()
            await s.close()
            self.ack_message(basic_deliver.delivery_tag)

    def ack_message(self, delivery_tag):
        self.logger.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def nack_message(self, delivery_tag):
        self.logger.info('Nack message %s', delivery_tag)
        self._channel.basic_nack(delivery_tag)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        if self._channel:
            self.logger.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            cb = functools.partial(self.on_cancelok, userdata=self._consumer_tag)
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
        self.logger.info('RabbitMQ acknowledged the cancellation of the consumer: %s', userdata)
        self.close_channel()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        self.logger.info('Closing the channel')
        self._channel.close()

    def run(self):
        self._connection = self.connect()

    def stop(self):
        if not self._closing:
            self._closing = True
            self.logger.info('Stopping')
            if self._consuming:
                self.stop_consuming()
            else:
                self._connection.ioloop.stop()
            self.logger.info('Stopped')


class PersonalChequeActivationConsumer(object):
    from rabbit import Queue
    QUEUE = Queue.PERSONAL_CHEQUE_ACTIVATION.value

    def __init__(self, url, loop, prefetch_count):
        self.logger = logging.getLogger(__class__.__name__)

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
        self.logger.info('Connecting to %s', self._url)
        return AsyncioConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
            custom_ioloop=self._outer_async_loop)

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            self.logger.info('Connection is closing or already closed')
        else:
            self.logger.info('Closing connection')
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        self.logger.info('Connection opened')
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err: BaseException):
        self.logger.error('Connection open failed: %s', err)
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason: BaseException):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self.logger.warning('Connection closed, reconnect necessary: %s', reason)
            self.reconnect()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        self.logger.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.logger.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()

    def add_on_channel_close_callback(self):
        self.logger.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)
        self.setup_queue(self.QUEUE)

    def on_channel_closed(self, channel, reason):
        self.logger.warning('Channel %i was closed: %s', channel, reason)
        self.close_connection()

    def setup_queue(self, queue_name):
        self.logger.info('Declaring queue %s', queue_name)
        cb = functools.partial(self.on_queue_declareok, userdata=queue_name)
        self._channel.queue_declare(queue=queue_name, callback=cb, durable=True)

    def on_queue_declareok(self, _unused_frame, userdata):
        queue_name = userdata
        self.logger.info('Queue %s has been declared successfully', queue_name)
        self.set_qos()

    def set_qos(self):
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        self.logger.info('QOS set to: %d', self._prefetch_count)
        self.start_consuming()

    def start_consuming(self):
        self.logger.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.QUEUE, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        self.logger.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        self.logger.info('Consumer was cancelled remotely, shutting down: %r',
                         method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        self.logger.info('Received message # %s from %s: %s', basic_deliver.delivery_tag, properties.app_id, body.decode())
        try:
            json_data = body.decode()
            self.logger.info(f"Decoded JSON: {json_data}")

            acd = ActivationPersonalChequeDto.model_validate_json(json_data)
            self._outer_async_loop.create_task(self.__process_activation(acd, basic_deliver))
        except Exception as e:
            self.logger.error(f"Failed to process message: {e}")
            self.logger.debug(f"Stack trace: {traceback.format_exc()}")
            self.nack_message(basic_deliver.delivery_tag)

    async def __process_activation(self, dto: ActivationPersonalChequeDto, basic_deliver) -> None:
        self.logger.info("Start cheque activation: %s", dto)
        s = get_session()
        await s.begin()
        a = await get_cheque_activation(dto.cheque_activation_id, s=s)
        self.logger.info(str(a))
        c = await cheque.get_active(dto.cheque_id)

        try:
            if not c.is_connected_to_user(dto.user_id) and c.is_creator(dto.user_id):
                a.status = ChequeActivationStatus.FAILED
                a.failed_message = "The cheque is intended for another user."
                self.logger.warning("Cheque activation failed for user_id %s - cheque intended for another user.", dto.user_id)

            else:
                uid = await make_transaction_from_system(
                    target=dto.user_id,
                    operation=TransactionOperation.INCREMENT,
                    amount=c.entity.amount,
                    created_by=dto.user_id,
                    description='cheque activation payout',
                    trace=generate_trace(TraceType.CHEQUE, str(c.entity.trace_uuid)),
                    session=s,
                    currency_type=c.entity.currency_type,
                    auto_commited=False
                )
                self.logger.info("Transaction successful with ID %s for user_id %s, cheque_id %s, amount %s, currency_type %s",
                                 uid, dto.user_id, dto.cheque_id, c.entity.amount, c.entity.currency_type)

                a.status = ChequeActivationStatus.COMPLETED
                a.payout_transaction_id = uid

                self.logger.info(f"Personal cheque has been processed successfully: %s", dto)

        except Exception as e:
            a.status = MailingMessageStatus.FAILED
            a.failed_message = str(e)
            self.logger.error(f"Failed to process the message: {dto} with error: {e}")
            self.logger.debug(f"Stack trace: {traceback.format_exc()}")
        finally:
            a.processed_at = now()
            await s.commit()
            await s.close()
            self.ack_message(basic_deliver.delivery_tag)

    def ack_message(self, delivery_tag):
        self.logger.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def nack_message(self, delivery_tag):
        self.logger.info('Nack message %s', delivery_tag)
        self._channel.basic_nack(delivery_tag)

    def stop_consuming(self):
        if self._channel:
            self.logger.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            cb = functools.partial(self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        self._consuming = False
        self.logger.info('RabbitMQ acknowledged the cancellation of the consumer: %s', userdata)
        self.close_channel()

    def close_channel(self):
        self.logger.info('Closing the channel')
        self._channel.close()

    def run(self):
        self._connection = self.connect()

    def stop(self):
        if not self._closing:
            self._closing = True
            self.logger.info('Stopping')
            if self._consuming:
                self.stop_consuming()
            else:
                self._connection.ioloop.stop()
            self.logger.info('Stopped')
