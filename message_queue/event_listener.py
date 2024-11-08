# message_queue/event_listener.py
from config import consumer
from message_queue.event_processor import process_event

def listen_for_events():
    for message in consumer:
        event = message.value.decode('utf-8')  # Asumiendo que los eventos están en JSON o texto
        process_event(event)
