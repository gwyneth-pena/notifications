

from producers.schemas import NotificationSchema


class NotificationUseCase:
    def __init__(self, producer):
        self.__producer = producer

    
    def send_notification(self, application_id, template_code, recipient, payload, type):
        """ Sends a notification to Kafka """

        self.__producer.send(application_id=application_id, payload=NotificationSchema(template_code=template_code, recipient=recipient, payload=payload, type=type))
