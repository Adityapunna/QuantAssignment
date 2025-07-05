from datetime import datetime, date
from sqlalchemy import DateTime, Date
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    subscription_tier = Column(String)  # Free, Pro, Premium
    requests_today = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_request_date = Column(Date, default=None, nullable=True)
