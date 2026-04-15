from app.database import SessionLocal
from app.models import Feedback
from sqlalchemy import func

db = SessionLocal()

try:
    # --- Feedback ---
    fb1 = Feedback(
        subscription_id=1,
        user_id=1,
        rating=5,
        comment="Excellent service!"
    )

    fb2 = Feedback(
        subscription_id=1,
        user_id=1,
        rating=4,
        comment="Very good, but can improve"
    )

    fb3 = Feedback(
        subscription_id=2,
        user_id=2,
        rating=3,
        comment="Average experience"
    )

    db.add_all([fb1, fb2, fb3])
    db.commit()

    # --- STATS (runtime calculation) ---
    stats_data = db.query(
        Feedback.subscription_id,
        func.avg(Feedback.rating).label("avg_rating"),
        func.count(Feedback.feedback_id).label("total_reviews")
    ).group_by(Feedback.subscription_id).all()

    for row in stats_data:
        print(
            f"Subscription {row.subscription_id}: "
            f"avg_rating={row.avg_rating}, "
            f"total_reviews={row.total_reviews}"
        )

finally:
    db.close()