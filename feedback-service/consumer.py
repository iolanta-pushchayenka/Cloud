import time
import json
from azure.servicebus import ServiceBusClient

from dotenv import load_dotenv
import os

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
QUEUE_NAME = os.getenv("QUEUE_NAME")


def process_message(data):
    print("Получено сообщение:", data)

    if data.get("event") == "subscription_created":
        print(f"Новая подписка: {data.get('subscription_id')}")
        print("Создаём feedback запись...")

def receive_messages():
    with ServiceBusClient.from_connection_string(CONNECTION_STRING) as client:
        with client.get_queue_receiver(queue_name=QUEUE_NAME) as receiver:

            messages = receiver.receive_messages(
                max_message_count=10,
                max_wait_time=5
            )

            for message in messages:
                body = b"".join(message.body).decode("utf-8")

                try:
                    data = json.loads(body)
                except:
                    data = {"raw": body}

                process_message(data)

                receiver.complete_message(message) 

if __name__ == "__main__":
    print("Consumer запущен и слушает очередь...")

    while True:
        receive_messages()
        time.sleep(5)