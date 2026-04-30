from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

Base = declarative_base()


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = {"schema": "SubscriptionService"}

    subscription_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    status = Column(String)
    plan_type = Column(String)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    renewal_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


class SubscriptionItems(Base):
    __tablename__ = "subscription_items"
    __table_args__ = {"schema": "SubscriptionService"}

    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey(
        "SubscriptionService.subscriptions.subscription_id"))
    ingredient_id = Column(Integer)
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
