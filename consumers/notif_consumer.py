import threading
from consumers.plugins.email_sender import EmailSender
from consumers.plugins.kafka_consumer import KafkaConsumer


stop_event = threading.Event()

email_sender = EmailSender()

def consume_notification(group_id, topic):
    consumer = KafkaConsumer(group_id, topic)

    for msg in consumer.consume():
        if stop_event.is_set():
            break
        try:
            if msg is None:
                continue

            email_sender.send(
                email="gwenpenadev@gmail.com",
                subject="Test email",
                template_file_name="welcome.html",
                template_data={"message": msg.decode("utf-8")}
            )
            print(f"Received message: {msg}")
            consumer.commit()
        except Exception as e:
            print(f"Error: {e}")
            continue


