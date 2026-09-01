from consumers.plugins.db import get_db
from fastapi import APIRouter, Depends, Request
from producers.auth import auth_required
from producers.schemas import NotificationSchema
from producers.use_cases import NotificationUseCase
from producers.repos import NotificationRepo
from shared.exceptions import APIException
from sqlalchemy.orm import Session



def get_notification_use_case(
    request: Request, 
):
    producer = request.app.state.kafka_producer
    return NotificationUseCase(producer)

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/send")
@auth_required
def send_notification(request: Request, payload: NotificationSchema, use_case: NotificationUseCase = Depends(get_notification_use_case)):
    """ Sends a notification to Kafka """

    auth_info = request.state.auth_info
    if not auth_info:
        return APIException(status_code=401, msg="Not authenticated")

    use_case.send_notification(auth_info.id, payload.template_code, payload.recipient, payload.payload, payload.type)
    return {"status": "ok"}

