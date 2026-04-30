from app.database import SessionLocal
from app.models import Subscription, SubscriptionItems
from datetime import datetime

db = SessionLocal()

try:
    # --- Subscription ---
    sub1 = Subscription(
        user_id=1,
        status="active",
        plan_type="monthly",
        start_date=datetime.utcnow()
    )

    sub2 = Subscription(
        user_id=2,
        status="paused",
        plan_type="weekly",
        start_date=datetime.utcnow()
    )

    db.add_all([sub1, sub2])
    db.commit()

    db.refresh(sub1)
    db.refresh(sub2)

    item1 = SubscriptionItems(
        subscription_id=sub1.subscription_id,
        ingredient_id=1,   # Tomato
        quantity=2
    )

    item2 = SubscriptionItems(
        subscription_id=sub1.subscription_id,
        ingredient_id=2,   # Cheese
        quantity=1
    )

    item3 = SubscriptionItems(
        subscription_id=sub2.subscription_id,
        ingredient_id=1,   # Tomato
        quantity=3
    )

    db.add_all([item1, item2, item3])
    db.commit()

finally:
    db.close()
