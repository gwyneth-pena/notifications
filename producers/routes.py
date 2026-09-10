from fastapi import APIRouter, Depends, Request
from producers.schemas import NotificationSchema
from producers.use_cases import NotificationUseCase
from shared.exceptions import APIException
from shared.auth import get_current_user


def get_notification_use_case(
    request: Request, 
):
    producer = request.app.state.kafka_producer
    return NotificationUseCase(producer)

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/send")
def send_notification(payload: NotificationSchema, use_case: NotificationUseCase = Depends(get_notification_use_case), auth_info = Depends(get_current_user)):
    """ Sends a notification to Kafka """

    use_case.send_notification(auth_info['id'], payload.template_code, payload.recipient, payload.payload, payload.type)
    return {"status": "ok"}

