from protobuf.message_pb2 import Message
from rabbit.conf import channel, message_exchange


def publish_message(body: Message):
    channel.basic_publish(exchange=message_exchange, body=body.SerializeToString())
