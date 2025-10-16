import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import os
from datetime import date

# ---------- Load Existing Expenses ----------
def load_expenses(filename="expenses.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

expenses = load_expenses()

# ---------- Predefined Categories ----------
categories = ["Food", "Transport", "Entertainment", "Bills", "Shopping"]

# ---------- Functions ----------

def save_expenses():
    with open("expenses.json", "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense():
    try:
        amount = float(amount_entry.get())
        category = category_var.get().strip().capitalize()
        date_val = date_entry.get()
        
        if not category or not date_val:
            messagebox.showerror("Error", "Category and Date cannot be empty.")
            return
        
        expenses.append({"amount": amount, "category": category, "date": date_val})
        
        if category not in categories:
            categories.append(category)
            category_combobox['values'] = categories
        
        save_expenses()
        messagebox.showinfo("Success", "Expense added successfully!")
        
        amount_entry.delete(0, tk.END)
        category_combobox.set("")
        date_entry.set_date(date.today())
        
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for amount.")

def show_total():
    total = sum(e["amount"] for e in expenses)
    messagebox.showinfo("Total Expenses", f"Total: ₹{total}")

def show_by_category():
    summary = {}
    for e in expenses:
        cat = e["category"]
        summary[cat] = summary.get(cat, 0) + e["amount"]
    
    if summary:
        sorted_summary = dict(sorted(summary.items(), key=lambda item: item[1], reverse=True))
        msg = "\n".join([f"{cat}: ₹{amt}" for cat, amt in sorted_summary.items()])
        messagebox.showinfo("Category-wise Summary", msg)
    else:
        messagebox.showinfo("Category-wise Summary", "No expenses yet.")

def clear_data():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all expenses?"):
        expenses.clear()
        if os.path.exists("expenses.json"):
            os.remove("expenses.json")
        messagebox.showinfo("Cleared", "All expense data has been cleared!")

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("400x450")

# Amount Input
tk.Label(root, text="Amount (₹):").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

# Category Input
tk.Label(root, text="Category:").pack()
category_var = tk.StringVar()
category_combobox = ttk.Combobox(root, textvariable=category_var)
category_combobox['values'] = categories
category_combobox.pack()
category_combobox.set("")

# Date Input
tk.Label(root, text="Date:").pack()
date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
date_entry.pack()

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)
tk.Button(root, text="Show Total", command=show_total).pack(pady=5)
tk.Button(root, text="Show by Category", command=show_by_category).pack(pady=5)
tk.Button(root, text="Clear All Data", fg="white", bg="red", command=clear_data).pack(pady=5)
tk.Button(root, text="Save & Exit", command=lambda: [save_expenses(), root.destroy()]).pack(pady=5)

root.mainloop()
