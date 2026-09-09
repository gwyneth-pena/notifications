
from consumers.plugins.db import get_db
from consumers.repos import NotificationRepo
from consumers.use_cases import ConsumerUseCase
from fastapi import APIRouter, Depends, Request
from shared.auth import auth_required


def get_consumer_use_case():
    session = next(get_db())
    repo = NotificationRepo(session)
    return ConsumerUseCase(repo)

router = APIRouter(prefix="/consumers", tags=["consumers"])

@router.get("/failed-requests")
@auth_required
def get_failed_requests(request: Request, use_case: ConsumerUseCase = Depends(get_consumer_use_case)):
    """ Gets failed requests from DB """
    auth_info = request.state.auth_info

    return use_case.get_failed(auth_info.id)

