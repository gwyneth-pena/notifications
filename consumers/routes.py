
from shared.db import get_db
from consumers.repos import NotificationRepo
from consumers.use_cases import ConsumerUseCase
from fastapi import APIRouter, Depends
from shared.auth import get_current_user

#TODO: Add auth LRU cache
def get_consumer_use_case(session = Depends(get_db)):
    repo = NotificationRepo(session)
    return ConsumerUseCase(repo)

router = APIRouter(prefix="/consumers", tags=["consumers"])

@router.get("/failed-requests")
def get_failed_requests(use_case: ConsumerUseCase = Depends(get_consumer_use_case), auth_info = Depends(get_current_user)):
    """ Gets failed requests from DB """

    return use_case.get_failed(auth_info.id)

@router.post("/trigger-notfications-reprocessing")
def trigger_notifications_reprocessing(use_case: ConsumerUseCase = Depends(get_consumer_use_case), auth_info = Depends(get_current_user)):
    """ Triggers notifications reprocessing """

    use_case.trigger_notifications_reprocessing(auth_info.id)
    return {"status": "ok"}

