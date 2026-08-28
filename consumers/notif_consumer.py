import threading
from consumers.plugins.kafka_consumer import KafkaConsumer


stop_event = threading.Event()

def consume_notification(group_id, topic):
    consumer = KafkaConsumer(group_id, topic)

    for msg in consumer.consume():
        if stop_event.is_set():
            break
        try:
            if msg is None:
                continue
            print(f"Received message: {msg}")
        except Exception as e:
            print(f"Error: {e}")
            continue


