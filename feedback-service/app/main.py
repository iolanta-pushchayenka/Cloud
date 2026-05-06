# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# from sqlalchemy import func
# from contextlib import asynccontextmanager

# import logging

# import app.database as database
# from app.models import Feedback


# print(">>> main.py: start import")

# import app.database as database
# print(">>> main.py: after database import")

# from app.models import Feedback
# print(">>> main.py: after models import")


# # ---------------- lifespan (FIX) ----------------
# @asynccontextmanager
# def lifespan(app: FastAPI):
#     database.init_db()
#     yield


# app = FastAPI(lifespan=lifespan)


# # ---------------- logging ----------------
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# logger = logging.getLogger(__name__)


# # ---------------- DB dependency ----------------
# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # ---------------- endpoints ----------------
# @app.get("/feedback")
# def get_feedback(db: Session = Depends(get_db)):
#     logger.info("Fetching feedback list")
#     return db.query(Feedback).all()


# @app.get("/feedback/stats")
# def get_feedback_stats(db: Session = Depends(get_db)):
#     logger.info("Fetching feedback statistics")

#     stats = db.query(
#         Feedback.subscription_id,
#         func.avg(Feedback.rating).label("avg_rating"),
#         func.count(Feedback.feedback_id).label("total_reviews")
#     ).group_by(Feedback.subscription_id).all()

#     return [
#         {
#             "subscription_id": s.subscription_id,
#             "avg_rating": float(s.avg_rating),
#             "total_reviews": s.total_reviews
#         }
#         for s in stats
#     ]


from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

import logging

import app.database as database
from app.models import Feedback

# ---------------- app ----------------
app = FastAPI()

# ---------------- logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------- DB dependency ----------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- endpoints ----------------
@app.get("/feedback")
def get_feedback(db: Session = Depends(get_db)):
    logger.info("Fetching feedback list")
    return db.query(Feedback).all()


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