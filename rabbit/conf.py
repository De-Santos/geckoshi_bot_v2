import os
from enum import Enum

import pika


class Queue(Enum):
    MESSAGE = "message-queue"
    PERSONAL_CHEQUE_ACTIVATION = "personal-cheque-activation-queue"


parameters = pika.URLParameters(os.getenv("RABBIT_URL"))
# connection = pika.BlockingConnection(parameters=parameters)
#
# channel = connection.channel()
#
# channel.queue_declare(queue=Queue.MESSAGE.value, durable=True)
# channel.basic_qos(prefetch_count=1)
