from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models import Feedback

import logging

# ---------------- logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------- app ----------------
app = FastAPI()

# ---------------- DB dependency ----------------


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- GET /feedback ----------------


@app.get("/feedback")
def get_feedback(db: Session = Depends(get_db)):
    logger.info("Fetching feedback list")
    return db.query(Feedback).all()

# ---------------- GET /feedback/stats ----------------


@app.get("/feedback/stats")
def get_feedback_stats(db: Session = Depends(get_db)):
    logger.info("Fetching feedback statistics")

    stats = db.query(
        Feedback.subscription_id,
        func.avg(Feedback.rating).label("avg_rating"),
        func.count(Feedback.feedback_id).label("total_reviews")
    ).group_by(Feedback.subscription_id).all()

    return [
        {
            "subscription_id": s.subscription_id,
            "avg_rating": float(s.avg_rating),
            "total_reviews": s.total_reviews
        }
        for s in stats
    ]
