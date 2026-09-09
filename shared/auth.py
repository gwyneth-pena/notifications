from fastapi import Depends, Header
from sqlalchemy.orm import Session
from shared.db import get_db
from shared.repos import AuthRepo
from shared.exceptions import APIException

def get_current_user(
    x_api_key: str = Header(..., alias="x-api-key"), 
    db: Session = Depends(get_db)
):
    if not x_api_key:
        raise APIException(status_code=401, msg="Not authenticated")

    auth_info = AuthRepo(db).get_auth_info_by_key(x_api_key)
    if not auth_info:
        raise APIException(status_code=401, msg="Not authenticated")

    return auth_info