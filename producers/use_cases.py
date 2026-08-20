

from producers.schemas import NotificationSchema


class NotificationUseCase:
    def __init__(self, repo, producer):
        self.__repo = repo
        self.__producer = producer
        self.__topics = {
            'email': 'notifications.email',
            'push': 'notifications.push'
        }
    
    def send_notification(self, tenant_id, recipient, message, type):
        """ Sends a notification to Kafka """

        #TODO: validate tenant_id, recipient, message, type
        self.__producer.send(topic=self.__topics[type], payload=NotificationSchema(tenant_id=tenant_id, recipient=recipient, message=message, type=type))
