from sqlalchemy import Column, Integer, ForeignKey
from backend.db.database import Base

class ListItem(Base):
    __tablename__ = 'list_items'

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('lists.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    index_in_list = Column(Integer)
