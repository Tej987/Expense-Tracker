import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x600")
        self.root.configure(bg="#eaeaea")

        self.expenses = []
        self.load_expenses()

        # Create a frame for the input fields
        frame = tk.Frame(self.root, bg="#ffffff")
        frame.pack(pady=20)

        # Description label and entry
        self.description_label = tk.Label(frame, text="Description:", bg="#ffffff", font=("Arial", 12))
        self.description_label.grid(row=0, column=0, sticky="w")
        self.description_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.description_entry.grid(row=0, column=1)

        # Amount label and entry
        self.amount_label = tk.Label(frame, text="Amount:", bg="#ffffff", font=("Arial", 12))
        self.amount_label.grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.amount_entry.grid(row=1, column=1)

        # Category label and entry
        self.category_label = tk.Label(frame, text="Category:", bg="#ffffff", font=("Arial", 12))
        self.category_label.grid(row=2, column=0, sticky="w")
        self.category_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.category_entry.grid(row=2, column=1)

        # Date label and entry
        self.date_label = tk.Label(frame, text="Date (YYYY-MM-DD):", bg="#ffffff", font=("Arial", 12))
        self.date_label.grid(row=3, column=0, sticky="w")
        self.date_entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.date_entry.grid(row=3, column=1)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default to today

        # Add expense button
        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.add_button.pack(pady=10)

        # Clear expenses button
        self.clear_button = tk.Button(self.root, text="Clear Expenses", command=self.clear_expenses, bg="#FF5733", fg="white", font=("Arial", 12))
        self.clear_button.pack(pady=10)

        # Listbox to display expenses
        self.expense_listbox = tk.Listbox(self.root, width=70, height=15, font=("Arial", 12))
        self.expense_listbox.pack(pady=10)

        # Total label
        self.total_label = tk.Label(self.root, text="Total Expenses: $0.00", bg="#eaeaea", font=("Arial", 14, "bold"))
        self.total_label.pack(pady=10)

        self.update_expense_listbox()
        self.update_total()

    def add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if description and amount and category and date:
            try:
                amount = float(amount)
                self.expenses.append({"description": description, "amount": amount, "category": category, "date": date})
                self.save_expenses()
                self.update_expense_listbox()
                self.update_total()
                self.clear_entries()
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid amount.")
        else:
            messagebox.showwarning("Warning", "All fields must be filled.")

    def clear_entries(self):
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Reset to today

    def clear_expenses(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all expenses?"):
            self.expenses.clear()
            self.save_expenses()
            self.update_expense_listbox()
            self.update_total()

    def update_expense_listbox(self):
        self.expense_listbox.delete(0, tk.END)
        for expense in self.expenses:
            self.expense_listbox.insert(tk.END, f"{expense['date']} - {expense['description']} - ${expense['amount']:.2f} ({expense['category']})")

    def update_total(self):
        total = sum(expense['amount'] for expense in self.expenses)
        self.total_label.config(text=f"Total Expenses: ${total:.2f}")

    def save_expenses(self):
        with open('expenses.json', 'w') as f:
            json.dump(self.expenses, f)

    def load_expenses(self):
        if os.path.exists('expenses.json'):
            with open('expenses.json', 'r') as f:
                self.expenses = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    expense_tracker = ExpenseTracker(root)
    root.mainloop()