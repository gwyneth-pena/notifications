
from producers.schemas import NotificationSchema
from shared.db_models import Application


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

