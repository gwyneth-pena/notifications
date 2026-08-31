from config import settings
from confluent_kafka import Consumer


class KafkaConsumer:
    def __init__(self, group_id, topic):
        consumer = Consumer({
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "security.protocol": settings.kafka_security_protocol,
            "sasl.mechanisms": settings.kafka_sasl_mechanism,
            "sasl.username": settings.kafka_sasl_username,
            "sasl.password": settings.kafka_sasl_password,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False
        })
        self.__consumer = consumer
        self.__topic = topic


    def consume(self):
        """ Consume messages from Kafka """

        self.__consumer.subscribe([self.__topic])

        try:
            while True:
                msg = self.__consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    yield None
                if msg.topic() == self.__topic:
                    yield msg.value()
        finally:
            self.__consumer.close()

    def commit(self):
        self.__consumer.commit()