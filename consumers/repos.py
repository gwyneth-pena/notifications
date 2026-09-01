

from shared.db_models import NotificationTemplate
from shared.models import NotificationTemplateModel


class NotificationRepo:
    def __init__(self, db_session):
        self.__db_session = db_session
        
    def get_template(self, application_id: str, template_code: str):
        """ Get Notification Templates """

        res = self.__db_session.query(NotificationTemplate).filter(
            NotificationTemplate.application_id == application_id,
            NotificationTemplate.code == template_code,
            NotificationTemplate.is_active == True
        ).first()

        return NotificationTemplateModel(id=res.id, application_id=res.application_id, code=res.code, subject=res.subject, template_path=res.template_path, sender_name=res.sender_name, sender_email=res.sender_email, reply_to=res.reply_to, is_active=res.is_active) if res else None

    def save_notification(self):
        """ Save Notification """
        pass