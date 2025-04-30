from sqlalchemy import Column, Integer, String
from backend.db.database import Base

class PayTier(Base):
    __tablename__ = 'pay_tiers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    token_quota = Column(Integer, default=1000)
