from sqlalchemy import Column, Integer, ForeignKey
from backend.core.database import Base

class UserList(Base):
    __tablename__ = 'user_lists'

    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey('lists.id'))
    user_id = Column(Integer, ForeignKey('users.id'))