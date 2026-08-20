from fastapi import APIRouter, Depends, Request
from producers.schemas import NotificationSchema
from producers.use_cases import NotificationUseCase
from producers.repos import NotificationRepo



def get_notification_use_case(request: Request):
    db_session = 'session'
    producer = request.app.state.kafka_producer
    return NotificationUseCase(NotificationRepo(db_session), producer )


router = APIRouter(prefix="/notifications", tags=["notifications"])

#TODO: add auth, create a decorator for auth
@router.post("/send")
def send_notification(payload: NotificationSchema, use_case: NotificationUseCase = Depends(get_notification_use_case)):
    """ Sends a notification to Kafka """
    use_case.send_notification(payload.tenant_id, payload.recipient, payload.message, payload.type)
    return {"status": "ok"}

