from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Subscription, SubscriptionItems, Base
from app.database import engine

from pydantic import BaseModel
import logging
import requests
import os
import json

# ---------------- logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------- app ----------------
app = FastAPI()

# ✅ СОЗДАНИЕ ТАБЛИЦ (КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ)
Base.metadata.create_all(bind=engine)

# ---------------- config ----------------
INGREDIENT_SERVICE_URL = "http://ingredient-service:3000"


# ---------------- schemas ----------------
class SubscriptionCreate(BaseModel):
    user_id: int
    plan_type: str


# ---------------- db dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- endpoints ----------------
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

    logger.info("Fetched subscriptions")
    return result


@app.post("/subscriptions")
def create_subscription(data: SubscriptionCreate, db: Session = Depends(get_db)):

    logger.info("Creating subscription request received")

    # ---------------- HTTP CALL ----------------
    try:
        ingredient_response = requests.get(
            f"{INGREDIENT_SERVICE_URL}/ingredients",
            timeout=3
        )
        ingredients = ingredient_response.json()
        logger.info("Fetched ingredients from IngredientService")

    except Exception as e:
        logger.error(f"IngredientService error: {e}")
        ingredients = []

    # ---------------- create subscription ----------------
    new_sub = Subscription(
        user_id=data.user_id,
        plan_type=data.plan_type,
        status="active"
    )

    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)

    # ---------------- send message ----------------
    send_message({
        "event": "subscription_created",
        "subscription_id": new_sub.subscription_id
    })

    return {
        "status": "created",
        "subscription_id": new_sub.subscription_id,
        "ingredients_preview": ingredients
    }


# ---------------- service bus ----------------
def send_message(data: dict):
    from azure.servicebus import ServiceBusClient, ServiceBusMessage

    connection_string = os.getenv("CONNECTION_STRING")
    queue_name = os.getenv("QUEUE_NAME")

    if not connection_string or not queue_name:
        logger.warning("ServiceBus not configured")
        return

    with ServiceBusClient.from_connection_string(connection_string) as client:
        sender = client.get_queue_sender(queue_name=queue_name)

        with sender:
            message = ServiceBusMessage(json.dumps(data))
            sender.send_messages(message)