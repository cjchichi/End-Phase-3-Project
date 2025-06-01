
from datetime import datetime
from lib.db.database import init_db, SessionLocal
from lib.models.expense import Expense
from lib.models.user import User
from lib.models.category import Category
from lib.utils.display import show_table

def main():
    init_db()
    session = SessionLocal()

    while True:
        print("\n=====Expense Tracker CLI=====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            username = input("User: ")
            user = session.query(User).filter_by(username=username).first()
            if not user:
                user = User(username=username)
                session.add(user)
                session.commit()

            category_name = input("Category: ")
            category = session.query(Category).filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                session.add(category)
                session.commit()

            data = {
                "date": datetime.strptime(input("Date (YYYY-MM-DD): "), "%Y-%m-%d"),
                "amount": float(input("Amount: ")),
                "description": input("Description: "),
                "user_id": user.id,
                "category_id": category.id,
            }

            Expense.add_expense(session, data)
            print("Expense added.")

        elif choice == "2":
            expenses = Expense.get_all(session)
            rows = [
                (e.id, e.date, e.user.username, e.category.name, e.amount, e.description) 
                for e in expenses
            ]
            show_table(rows, headers=["ID", "Date", "User", "Category", "Amount", "Description"])

        elif choice == "3":
            eid = int(input("Enter expense ID to update: "))
            updated_data = {
                "date": datetime.strptime(input("New Date (YYYY-MM-DD): "), "%Y-%m-%d"),
                "category":input("New Category:"),
                "amount": float(input("New Amount: ")),
                "description": input("New Description: "),
            }
            Expense.update_expense(session, eid, updated_data)
            print("Expense updated.")

        elif choice == "4":
            eid = int(input("Enter expense ID to delete: "))
            Expense.delete_expense(session, eid)
            print("Expense deleted.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
