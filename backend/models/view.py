from sqlalchemy import Column, Integer, ForeignKey, DateTime
from backend.db.database import Base

class View(Base):
    __tablename__ = 'views'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    view_count = Column(Integer, default=1)
    last_viewed = Column(DateTime, default='CURRENT_TIMESTAMP')
