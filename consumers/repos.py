import hashlib
import json
from typing import Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from shared.db_models import Notification, NotificationTemplate
from shared.models import NotificationModel, NotificationTemplateModel


class NotificationRepo:
    def __init__(self, db_session):
        self.__db_session = db_session

    def __to_notification_model(self, instance: Notification) -> NotificationModel:
        """Converts DB Notification model instance to domain NotificationModel."""
        return NotificationModel(
            id=instance.id,
            application_id=instance.application_id,
            template_id=instance.template_id,
            recipient=instance.recipient,
            channel=instance.channel,
            payload=instance.payload,
            status=instance.status,
            retry_count=instance.retry_count,
            max_retries=instance.max_retries,
            error_message=instance.error_message,
        )

    def get_template(
        self, application_id: str, template_code: str
    ) -> Optional[NotificationTemplateModel]:
        """Fetch active notification template."""
        res = (
            self.__db_session.query(NotificationTemplate)
            .filter(
                NotificationTemplate.application_id == application_id,
                NotificationTemplate.code == template_code,
                NotificationTemplate.is_active == True,
            )
            .first()
        )

        if not res:
            return None

        return NotificationTemplateModel(
            id=res.id,
            application_id=res.application_id,
            code=res.code,
            subject=res.subject,
            template_path=res.template_path,
            sender_name=res.sender_name,
            sender_email=res.sender_email,
            reply_to=res.reply_to,
            is_active=res.is_active,
        )

    def save_notification(
        self,
        application_id: str,
        template_id: str,
        recipient: str,
        channel: str,
        payload: dict,
        max_retries: int,
    ) -> Optional[NotificationModel]:
        """Save new notification with idempotency check."""
        raw_key = f"{application_id}:{template_id}:{recipient}:{json.dumps(payload, sort_keys=True)}"
        idempotency_key = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

        try:
            notification = Notification(
                application_id=application_id,
                template_id=template_id,
                idempotency_key=idempotency_key,
                recipient=recipient,
                channel=channel,
                payload=payload,
                max_retries=max_retries,
            )

            self.__db_session.add(notification)
            self.__db_session.commit()
            self.__db_session.refresh(notification)

            return self.__to_notification_model(notification)
        except IntegrityError:
            self.__db_session.rollback()
            notification = (
                self.__db_session.query(Notification)
                .filter(Notification.idempotency_key == idempotency_key)
                .first()
            )
            return self.__to_notification_model(notification) if notification else None
        except SQLAlchemyError:
            self.__db_session.rollback()
            return None

    def update_notification_status(
        self, notification_id: int, status: str, error_message: Optional[str] = None
    ) -> Optional[NotificationModel]:
        """Update status and optional error message for a notification."""
        notification = (
            self.__db_session.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )
        if not notification:
            return None

        notification.status = status
        notification.error_message = error_message
        self.__db_session.commit()
        self.__db_session.refresh(notification)

        return self.__to_notification_model(notification)

    def update_notification_retry_count(
        self, notification_id: int
    ) -> Optional[NotificationModel]:
        """Increment retry count for a notification."""
        notification = (
            self.__db_session.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )
        if not notification:
            return None

        notification.retry_count += 1
        self.__db_session.commit()
        self.__db_session.refresh(notification)

        return self.__to_notification_model(notification)