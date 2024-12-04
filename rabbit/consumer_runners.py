import os
from asyncio import AbstractEventLoop

from rabbit.consumers import MessageConsumer, PersonalChequeActivationConsumer, ChequePaybackConsumer, MultiChequeActivationConsumer


class MessageConsumerRunner:

    def __init__(self, loop: AbstractEventLoop):
        self._amqp_url = os.getenv("RABBIT_URL")
        self._prefetch_count = int(os.getenv("RABBIT_PREFETCH_COUNT"))
        self._loop = loop
        self._consumer = MessageConsumer(self._amqp_url, self._loop, self._prefetch_count)

    def run(self):
        self._consumer.run()

    def stop(self):
        self._consumer.stop()


class PersonalChequeActivationConsumerRunner:

    def __init__(self, loop: AbstractEventLoop):
        self._amqp_url = os.getenv("RABBIT_URL")
        self._prefetch_count = int(os.getenv("CHEQUE_PERSONAL_ACTIVATION_PREFETCH_COUNT"))
        self._loop = loop
        self._consumer = PersonalChequeActivationConsumer(self._amqp_url, self._loop, self._prefetch_count)

    def run(self):
        self._consumer.run()

    def stop(self):
        self._consumer.stop()


class MultiChequeActivationConsumerRunner:

    def __init__(self, loop: AbstractEventLoop):
        self._amqp_url = os.getenv("RABBIT_URL")
        self._prefetch_count = int(os.getenv("CHEQUE_MULTI_ACTIVATION_PREFETCH_COUNT"))
        self._loop = loop
        self._consumer = MultiChequeActivationConsumer(self._amqp_url, self._loop, self._prefetch_count)

    def run(self):
        self._consumer.run()

    def stop(self):
        self._consumer.stop()


class ChequePaybackConsumerRunner:

    def __init__(self, loop: AbstractEventLoop):
        self._amqp_url = os.getenv("RABBIT_URL")
        self._prefetch_count = int(os.getenv("CHEQUE_PAYBACK_PREFETCH_COUNT"))
        self._loop = loop
        self._consumer = ChequePaybackConsumer(self._amqp_url, self._loop, self._prefetch_count)

    def run(self):
        self._consumer.run()

    def stop(self):
        self._consumer.stop()
