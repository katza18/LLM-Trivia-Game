from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from backend.core.database import Base

class List(Base):
    __tablename__ = 'lists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    creator_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime)