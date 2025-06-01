from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    expenses = relationship("Expense", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
