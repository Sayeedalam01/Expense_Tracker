# expense.py

class Expense:
    def __init__(self, expense_id, amount, category, date, description):
        self.expense_id = expense_id
        self.amount = float(amount)
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "expense_id": self.expense_id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }

    def __str__(self):
        return f"ID: {self.expense_id} | Amount: ${self.amount:.2f} | Category: {self.category} | Date: {self.date} | Desc: {self.description}"