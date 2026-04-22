from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Subscription, SubscriptionItems
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json
from dotenv import load_dotenv
import os
from pydantic import BaseModel

class SubscriptionCreate(BaseModel):
    user_id: int
    plan_type: str

load_dotenv()

app = FastAPI()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
QUEUE_NAME = os.getenv("QUEUE_NAME")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/subscriptions")
def get_subscriptions(db: Session = Depends(get_db)):
    subscriptions = db.query(Subscription).all()

    result = []

    for sub in subscriptions:
        items = db.query(SubscriptionItems).filter(
            SubscriptionItems.subscription_id == sub.subscription_id
        ).all()

        result.append({
            "subscription_id": sub.subscription_id,
            "user_id": sub.user_id,
            "status": sub.status,
            "plan_type": sub.plan_type,
            "items": [
                {
                    "ingredient_id": i.ingredient_id,
                    "quantity": i.quantity
                }
                for i in items
            ]
        })

    return result

@app.post("/subscriptions")
def create_subscription(data: SubscriptionCreate, db: Session = Depends(get_db)):
    new_sub = Subscription(
        user_id=data.user_id,
        plan_type=data.plan_type,
        status="active"
    )

    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)

    # 🔥 ТРИГГЕР — отправка в очередь
    send_message({
        "event": "subscription_created",
        "subscription_id": new_sub.subscription_id
    })

    return {
        "status": "created",
        "subscription_id": new_sub.subscription_id
    }

def send_message(data: dict):
    with ServiceBusClient.from_connection_string(CONNECTION_STRING) as client:
        sender = client.get_queue_sender(queue_name=QUEUE_NAME)

        with sender:
            message = ServiceBusMessage(json.dumps(data))
            sender.send_messages(message)