import json
import threading
from consumers.plugins.db import get_db
from consumers.plugins.email_sender import EmailSender
from consumers.plugins.kafka_consumer import KafkaConsumer
from consumers.plugins.kafka_producer import KafkaProducer
from consumers.repos import NotificationRepo

stop_event = threading.Event()
email_sender = EmailSender()
dlq_producer = KafkaProducer()


def send_to_dead_letter_queue(application_id: str, notification_id: str):
    dlq_producer.send(application_id=application_id, notification_id=notification_id, topic='dlq')

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

            try:
                data = json.loads(msg.decode("utf-8") if isinstance(msg, bytes) else msg)
            except Exception as parse_err:
                print(f"Invalid JSON payload: {parse_err}")
                consumer.commit()
                continue

            application_id = data.get("application_id")
            template_code = data.get("template_code")
            msg_type = data.get("type")
            recipient = data.get("recipient")
            payload = data.get("payload", {})

            formatted_code = template_code.upper() if template_code else ""
            template = repo.get_template(application_id, formatted_code)
            if not template:
                consumer.commit()
                print(f"Template not found for code: {template_code}")
                continue

            notif = None

            try:
                notif = repo.save_notification(application_id, template.id, recipient, msg_type, payload, 3)

                if not notif:
                    consumer.commit()
                    continue

                if notif.status == "SENT":
                    consumer.commit()
                    continue

                if msg_type == "email":
                    email_sender.send(
                        email=recipient,
                        subject=template.subject,
                        template_file_name=template.template_path,
                        template_data={"payload": payload},
                        reply_to=[recipient],
                    )

                repo.update_notification_status(notif.id, "SENT")
                consumer.commit()
                print(f"Successfully processed message for recipient: {recipient}")
            except Exception as e:
                print(f"Error processing message: {e}")
                db_session.rollback()
                
                updated_notif = repo.update_notification_retry_count(notif.id)

                if updated_notif.retry_count >= updated_notif.max_retries and updated_notif.status=='RETRY':
                    updated_notif = repo.update_notification_status(notif.id, "FAILED", str(e))
                    send_to_dead_letter_queue(updated_notif.application_id, updated_notif.id)
                    consumer.commit()
                elif updated_notif.retry_count < updated_notif.max_retries and updated_notif.status!='RETRY':
                    updated_notif = repo.update_notification_status(notif.id, "RETRY", str(e))

        except Exception as e:
            print(f"Error processing message: {e}")
            db_session.rollback()
        finally:
            db_gen.close()