from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Subscription, SubscriptionItems

app = FastAPI()

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