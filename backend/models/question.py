from sqlalchemy import Column, Integer, String
from backend.db.database import Base

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    choice1 = Column(String)
    choice2 = Column(String)
    choice3 = Column(String)
    choice4 = Column(String)
    type = Column(String)
    topic = Column(String)
