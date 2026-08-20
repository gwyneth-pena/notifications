from config import settings
from confluent_kafka import Producer
from fastapi import status
from producers.schemas import NotificationSchema
from shared.exceptions import APIException


class KafkaProducer:

    def __init__(self):
        self.__kafka_producer = Producer({
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "security.protocol": settings.kafka_security_protocol,
            "sasl.mechanisms": settings.kafka_sasl_mechanism,
            "sasl.username": settings.kafka_sasl_username,
            "sasl.password": settings.kafka_sasl_password,
        })

    def send(self, topic: str, payload: NotificationSchema):
        """Sends a notification to Kafka"""
        delivery_error = None

        def _delivery_report(err, msg):
            nonlocal delivery_error
            if err is not None:
                delivery_error = err

        try:
            value_bytes = payload.model_dump_json(
                exclude_unset=True, exclude_none=True
            ).encode("utf-8")
            
            key_bytes = payload.tenant_id.encode("utf-8")

            self.__kafka_producer.produce(
                topic=topic,
                key=key_bytes,
                value=value_bytes,
                on_delivery=_delivery_report,
            )

            self.__kafka_producer.poll(0)
            self.__kafka_producer.flush(timeout=10)

            if delivery_error:
                raise Exception(f"Delivery failed: {delivery_error}")

        except Exception as e:
            raise APIException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg=str(e),
                location="kafka",
                type_="server_error",
            )