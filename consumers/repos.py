

import hashlib
import json
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from shared.db_models import Notification, NotificationTemplate
from shared.models import NotificationModel, NotificationTemplateModel


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

    def save_notification(self, application_id: str, template_id: str, recipient: str, channel: str, payload: dict, max_retries: int):
        """ Save Notification """

        idempotency_key = f"{application_id}:{template_id}:{recipient}:{json.dumps(payload)}"
    
        idempotency_key = hashlib.sha256(idempotency_key.encode("utf-8")).hexdigest()

        try:
            notication = Notification(
                application_id=application_id,
                template_id=template_id,
                idempotency_key=idempotency_key,
                recipient=recipient,
                channel=channel,
                payload=payload,
                max_retries=max_retries
            )

            self.__db_session.add(notication)
            self.__db_session.commit()
            self.__db_session.refresh(notication)

            return NotificationModel(
                id=notication.id,
                application_id=notication.application_id,
                template_id=notication.template_id,
                recipient=notication.recipient,
                channel=notication.channel,
                payload=notication.payload,
                status=notication.status,
                retry_count=notication.retry_count,
                max_retries=notication.max_retries,
                error_message=notication.error_message
            )
        except IntegrityError:
            self.__db_session.rollback()
            return None
        except SQLAlchemyError as e:
            self.__db_session.rollback()
            return None

    def update_notification_status(self, notification_id: int, status: str, error_message: str = None):
        """ Update Notification Status """

        notification = self.__db_session.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            return None

        notification.status = status
        notification.error_message = error_message
        self.__db_session.commit()
        self.__db_session.refresh(notification)

        return NotificationModel(
            id=notification.id,
            application_id=notification.application_id,
            template_id=notification.template_id,
            recipient=notification.recipient,
            channel=notification.channel,
            payload=notification.payload,
            status=notification.status,
            retry_count=notification.retry_count,
            max_retries=notification.max_retries,
            error_message=notification.error_message
        )