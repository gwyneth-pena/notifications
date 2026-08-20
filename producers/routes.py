from fastapi import APIRouter, Depends, Request
from producers.plugins.kafka_producer import KafkaProducer
from producers.schemas import NotificationSchema
from producers.use_cases import NotificationUseCase
from producers.repos import NotificationRepo



def get_notification_use_case(request: Request):
    db_session = 'session'
    return NotificationUseCase(NotificationRepo(db_session), KafkaProducer())


router = APIRouter(prefix="/notifications", tags=["notifications"])

#TODO: add auth, create a decorator for auth
@router.post("/send")
def send_notification(payload: NotificationSchema, use_case: NotificationUseCase = Depends(get_notification_use_case)):
    """ Sends a notification to Kafka """
    use_case.send_notification(payload.tenant_id, payload.recipient, payload.message, payload.type)
    return {"status": "ok"}

