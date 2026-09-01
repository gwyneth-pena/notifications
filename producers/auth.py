
from functools import wraps
from consumers.plugins.db import get_db
from fastapi import Request
from producers.repos import AuthRepo
from shared.exceptions import APIException


def auth_required(func):
    """ Auth Required """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_session = None
        try:
            request: Request = kwargs.get("request")
            
            api_key = request.headers.get("x-api-key")

            if not api_key:
                raise APIException(status_code=401, msg="Not authenticated")

            db_gen = get_db()
            db_session = next(db_gen)
            is_valid = AuthRepo(db_session).verify_api_key(api_key)

            if not is_valid:
                raise APIException(status_code=401, msg="Not authenticated")

            auth_info = AuthRepo(db_session).auth_info(api_key)

            request.state.auth_info = auth_info
            
        finally:
            if db_session:
                db_session.close()
    
        return func(*args, **kwargs)
    return wrapper