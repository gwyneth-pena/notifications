
from producers.schemas import NotificationSchema


class NotificationRepo:
    def __init__(self, db_session):
        self.__db_session = db_session
        

    def getTenantData(self, tenant_id):
        """ Get Tenant Data """
        pass

    