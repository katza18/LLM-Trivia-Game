from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from backend.db.database import Base

class TokenLog(Base):
    __tablename__ = 'token_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tokens_used = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
