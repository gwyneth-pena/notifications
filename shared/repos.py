
from shared.db_models import Application

class AuthRepo:
    def __init__(self, db_session):
        self.__db_session = db_session

    def get_auth_info_by_key(self, api_key):
        """ Get Auth Info """
        auth_info = self.__db_session.query(Application).filter(Application.api_key == api_key, Application.is_active == True).first()
        if not auth_info:
            return None
        
        auth_info = {
            "id": auth_info.id,
            "name": auth_info.name,
            "is_active": auth_info.is_active,
        }
        
        return auth_info

