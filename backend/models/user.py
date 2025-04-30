from sqlalchemy import Column, Integer, String, DateTime
from backend.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    pay_tier = Column(String, default='free')
    created_at = Column(DateTime)
    token_used = Column(Integer, default=0)
    quota_expiry = Column(DateTime)
