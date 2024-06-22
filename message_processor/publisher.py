from aiogram.types import Message as AiogramMessage
from confluent_kafka import Producer

from kafka_processor import register_producer, Topic
from kafka_processor.producer import proto_produce
from protobuf.message_pb2 import Message

__message_producer: Producer = register_producer()


async def send_message(parent_msg: AiogramMessage, text: str):
    proto_produce(Topic.MESSAGE, Message, Message(chat_id=parent_msg.chat.id, text=text))
