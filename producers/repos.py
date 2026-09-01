
from producers.schemas import NotificationSchema
from shared.db_models import Application
from shared.models import ApplicationModel


class NotificationRepo:
    def __init__(self, db_session):
        self.__db_session = db_session
        

    def getTenantData(self, tenant_id):
        """ Get Tenant Data """
        pass


class AuthRepo:
    def __init__(self, db_session):
        self.__db_session = db_session

    def verify_api_key(self, api_key):
        """ Verify API Key """

        return self.__db_session.query(Application).filter(Application.api_key == api_key, Application.is_active == True).first()

    def auth_info(self, api_key):
        """ Get Auth Info """
        auth_info = self.__db_session.query(Application).filter(Application.api_key == api_key, Application.is_active == True).first()
        auth_info = ApplicationModel(id=auth_info.id, name=auth_info.name, api_key=auth_info.api_key, is_active=auth_info.is_active) if auth_info else None
        return auth_info

