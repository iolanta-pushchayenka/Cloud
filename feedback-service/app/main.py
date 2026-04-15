from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models import Feedback

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/feedback")
def get_feedback(db: Session = Depends(get_db)):
    return db.query(Feedback).all()


@app.get("/feedback/stats")
def get_feedback_stats(db: Session = Depends(get_db)):
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