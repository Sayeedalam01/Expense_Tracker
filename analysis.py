import numpy as np

def calculate_summary(expenses_list):
    if not expenses_list:
        return "No data available to analyze."
    amounts = [expense.amount for expense in expenses_list]
    
    amounts_array = np.array(amounts)
    
    total = np.sum(amounts_array)
    average = np.mean(amounts_array)
    highest = np.max(amounts_array)
    lowest = np.min(amounts_array)
    
    summary_text = (
        f"\n--- NumPy Expense Analysis ---\n"
        f"Total Spent: ${total:.2f}\n"
        f"Average Expense: ${average:.2f}\n"
        f"Highest Expense: ${highest:.2f}\n"
        f"Lowest Expense: ${lowest:.2f}\n"
    )
    return summary_text