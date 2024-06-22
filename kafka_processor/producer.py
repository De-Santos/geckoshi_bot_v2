import logging
from uuid import uuid4

from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField

from kafka_processor import register_producer, Topic

__message_producer: Producer = register_producer()


def delivery_callback(err, msg):
    if err:
        logging.exception("Message failed delivery: {}".format(err))
    else:
        logging.info("Produced event to topic {topic}: key = {key:12}".format(
            topic=msg.topic(), key=msg.key().decode('utf-8')))


def proto_produce(topic: Topic, c_type: type, obj):
    string_serializer = StringSerializer('utf8')
    schema_registry_conf = {
        "url": "https://psrc-2312y.europe-west3.gcp.confluent.cloud",
        "basic.auth.user.info": "5L3VC72DO7E3NWLY:YrLTN/WHLC8PazsxbKTt6n93BBiKLUpyw+l/lRzaLM8JHsqj1VjPePris/3g6As0",
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    protobuf_serializer = ProtobufSerializer(c_type, schema_registry_client, {'use.deprecated.format': False})
    __message_producer.produce(topic.value, key=string_serializer(str(uuid4())),
                               value=protobuf_serializer(obj, SerializationContext(topic.value, MessageField.VALUE)),
                               callback=delivery_callback)
    __message_producer.poll(1000)
    __message_producer.flush()

