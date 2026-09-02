import json
import threading
from consumers.plugins.db import get_db
from consumers.plugins.email_sender import EmailSender
from consumers.plugins.kafka_consumer import KafkaConsumer
from consumers.repos import NotificationRepo

stop_event = threading.Event()
email_sender = EmailSender()


def consume_notification(group_id, topic):
    consumer = KafkaConsumer(group_id, topic)

    for msg in consumer.consume():
        if stop_event.is_set():
            break

        if msg is None:
            continue

        db_gen = get_db()
        db_session = next(db_gen)

        try:
            repo = NotificationRepo(db_session)

            data = json.loads(msg.decode("utf-8") if isinstance(msg, bytes) else msg)

            application_id = data.get("application_id")
            template_code = data.get("template_code")
            msg_type = data.get("type")
            recipient = data.get("recipient")
            payload = data.get("payload", {})

            template = repo.get_template(application_id, template_code.upper())
            if not template:
                print(f"Template not found for code: {template_code}")
                continue

            notif = repo.save_notification(application_id, template.id, recipient, msg_type, payload, 3)

            if not notif:
                print(f"Notification not saved for recipient: {recipient}")
                continue

            if msg_type == "email":
                email_sender.send(
                    email=recipient,
                    subject=template.subject,
                    template_file_name=template.template_path,
                    template_data={"payload": payload},
                    reply_to=[recipient],
                )

            consumer.commit()
            print(f"Successfully processed message for recipient: {recipient}")

            repo.update_notification_status(notif.id, "SENT")

        except Exception as e:
            print(f"Error processing message: {e}")
            db_session.rollback()
        finally:
            db_gen.close()