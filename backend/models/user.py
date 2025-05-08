from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())
    tokens_used = Column(Integer, default=0)
    quota = Column(Integer, default=0)
    quota_expiration = Column(DateTime)
