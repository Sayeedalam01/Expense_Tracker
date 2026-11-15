# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
from manager import ExpenseManager
from expense import Expense
from analysis import calculate_summary

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Team 3: Personal Expense Tracker")
        self.root.geometry("850x600")
        
        self.manager = ExpenseManager()
        
        try:
            self.manager.load_from_file()
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            messagebox.showwarning("Warning", "Data file is corrupted. Starting fresh.")

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        input_frame = tk.LabelFrame(self.root, text="Add New Expense", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        # ID
        tk.Label(input_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = tk.Entry(input_frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Amount
        tk.Label(input_frame, text="Amount:").grid(row=0, column=2, padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)

        # Category (Tuple)
        tk.Label(input_frame, text="Category:").grid(row=0, column=4, padx=5, pady=5)
        self.category_combo = ttk.Combobox(input_frame, values=self.manager.category_tuple, state="readonly")
        self.category_combo.grid(row=0, column=5, padx=5, pady=5)

        # Date
        tk.Label(input_frame, text="Date:").grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        # Description
        tk.Label(input_frame, text="Description:").grid(row=1, column=2, padx=5, pady=5)
        self.desc_entry = tk.Entry(input_frame)
        self.desc_entry.grid(row=1, column=3, padx=5, pady=5)

        # Add Button
        self.add_btn = tk.Button(input_frame, text="Add Expense", command=self.add_expense, bg="green", fg="white")
        self.add_btn.grid(row=1, column=5, padx=5, pady=5)

        # --- Table Frame ---
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("ID", "Amount", "Category", "Date", "Description")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True)

        # --- Button Frame 
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(btn_frame, text="Delete Selected", command=self.delete_expense, bg="red", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Show NumPy Summary", command=self.show_summary, bg="blue", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save & Exit", command=self.save_and_exit, bg="gray", fg="white").pack(side="right", padx=5)

    def add_expense(self):
        exp_id = self.id_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        category = self.category_combo.get()
        date = self.date_entry.get().strip()
        desc = self.desc_entry.get().strip()

        if not exp_id or not amount_str or not category or not date:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Exception handling for amount
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid amount! Must be a number greater than 0.")
            return

        new_expense = Expense(exp_id, amount, category, date, desc)
        
        if self.manager.add_expense(new_expense):
            messagebox.showinfo("Success", "Expense added successfully!")
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "ID already exists!")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for exp in self.manager.expenses_list:
            self.tree.insert("", tk.END, values=(exp.expense_id, exp.amount, exp.category, exp.date, exp.description))

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an expense to delete.")
            return
        
        item_values = self.tree.item(selected_item)['values']
        exp_id = str(item_values[0])
        
        if self.manager.delete_expense(exp_id):
            messagebox.showinfo("Success", "Expense deleted!")
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Could not delete expense.")

    def show_summary(self):
        summary = calculate_summary(self.manager.expenses_list)
        messagebox.showinfo("NumPy Analysis", summary)

    def save_and_exit(self):
        self.manager.save_to_file()
        messagebox.showinfo("Saved", "Data saved to JSON. Goodbye!")
        self.root.destroy()

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.category_combo.set('')

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()