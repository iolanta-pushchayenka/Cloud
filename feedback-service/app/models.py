from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = {"schema": "FeedbackService"}

    feedback_id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer)
    user_id = Column(Integer)
    rating = Column(Integer)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
