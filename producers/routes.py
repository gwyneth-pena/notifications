from consumers.plugins.db import get_db
from fastapi import APIRouter, Depends, Request
from producers.auth import auth_required
from producers.schemas import NotificationSchema
from producers.use_cases import NotificationUseCase
from producers.repos import NotificationRepo
from sqlalchemy.orm import Session



def get_notification_use_case(
    request: Request, 
    db: Session = Depends(get_db) 
):
    producer = request.app.state.kafka_producer
    return NotificationUseCase(NotificationRepo(db), producer)

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/send")
@auth_required
def send_notification(request: Request, payload: NotificationSchema, use_case: NotificationUseCase = Depends(get_notification_use_case)):
    """ Sends a notification to Kafka """
    use_case.send_notification(payload.tenant_id, payload.recipient, payload.message, payload.type)
    return {"status": "ok"}

