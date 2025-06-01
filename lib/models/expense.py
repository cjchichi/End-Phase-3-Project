    
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship, Session
from lib.db.database import Base
from lib.models.category import Category


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")

    def __repr__(self):
        return f"<Expense(id={self.id}, date={self.date}, amount={self.amount})>"

    @classmethod
    def add_expense(cls, session: Session, data: dict):
        expense = cls(
            date=data['date'],
            amount=data['amount'],
            description=data.get('description'),
            user_id=data['user_id'],
            category_id=data['category_id']
        )
        session.add(expense)
        session.commit()
        return expense

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def update_expense(cls, session: Session, expense_id: int, updated_data: dict):
        expense = session.get(cls, expense_id)
        if expense:
            for key, value in updated_data.items():
                if key == "user":
                    user_instance = session.query(User).filter_by(username=value).first()
                    if user_instance:
                        expense.user = user_instance
                    else:
                        print(f"User '{value}' not found.Please add the user first.")
                        return
                elif key == "category":
                    category_instance = session.query(Category).filter_by(name=value).first()
                    if not category_instance:
                        category_instance = Category(name=value)
                        session.add(category_instance)
                        session.commit()
                    expense.category = category_instance
                else:
                    setattr(expense, key, value)
            session.commit()
        return expense

    @classmethod
    def delete_expense(cls, session: Session, expense_id: int):
        expense = session.get(cls, expense_id)
        if expense:
            session.delete(expense)
            session.commit()
        return expense
