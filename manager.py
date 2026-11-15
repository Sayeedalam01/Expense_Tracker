# manager.py
import json
import os
from expense import Expense

class ExpenseManager:
    def __init__(self):
        self.expenses_list = []
        self.category_tuple = ("Food", "Transport", "Bills", "Shopping", "Other") # Tuple
        self.used_ids_set = set()
        self.expense_dict = {}
        self.file_name = "expenses_data.json"

    def add_expense(self, expense_obj):
        if expense_obj.expense_id in self.used_ids_set:
            return False 
        
        self.expenses_list.append(expense_obj)
        self.used_ids_set.add(expense_obj.expense_id)
        self.expense_dict[expense_obj.expense_id] = expense_obj
        return True

    def delete_expense(self, expense_id):
        if expense_id in self.expense_dict:
            del self.expense_dict[expense_id]
            self.used_ids_set.remove(expense_id)
            self.expenses_list = [e for e in self.expenses_list if e.expense_id != expense_id]
            return True
        return False

    def save_to_file(self):
        data = [expense.to_dict() for expense in self.expenses_list]
        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)

    def load_from_file(self):
        if not os.path.exists(self.file_name):
            return 
        
        with open(self.file_name, "r") as file:
            data = json.load(file)
            for item in data:
                exp = Expense(item["expense_id"], item["amount"], item["category"], item["date"], item["description"])
                self.expenses_list.append(exp)
                self.used_ids_set.add(exp.expense_id)
                self.expense_dict[exp.expense_id] = exp