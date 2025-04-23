from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    pay_tier = Column(String, default='free')
    auth_id = Column(String, unique=True)
    created_at = Column(DateTime)
    token_used = Column(Integer, default=0)
    quota_expiry = Column(DateTime)