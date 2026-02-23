expense_records = []        #stores each expense as a tuple(category, amount, date).
category_totals = {}        #to sum spending by category.
unique_categories = set()   #track all distinct categories.
overall_stats = {}

print("\n=== PERSONAL EXPENSE TRACKER ===")
for i in range(5):
    category = input(f"\nEnter expense {i+1} category: ")
    amount = float(input(f"Enter expense {i+1} amount: "))
    date = input(f"Enter expense {i+1} date (YYYY-MM-DD): ")

    expense_tuple = (category, amount, date)
    expense_records.append(expense_tuple)
    unique_categories.add(category)

    #x = (t[1] for t in expense_records)
    #x_float = float(x)
    category_totals[category] = category_totals.get(category, 0) + amount

total_spending = sum(t[1] for t in expense_records)
overall_stats['total'] = total_spending

total_expense_count = len(expense_records)
average_expense = total_spending/total_expense_count
overall_stats['average'] = average_expense

highest_expense = max(expense_records, key=lambda t: t[1])
overall_stats['highest'] = highest_expense

lowest_expense = min(expense_records, key=lambda t: t[1])
overall_stats['lowest'] = lowest_expense

print("\n=== OVERALL SPENDING SUMMARY ===")
print(f"Total Spending: ${total_spending:.2f}")
print(f"Average Expense: ${average_expense:.2f}")
print(f"Highest Expense: ${overall_stats['highest'][1]:.2f} (Category: {overall_stats['highest'][0].title()}, Date: {overall_stats['highest'][2]})")
print(f"Lowest Expense: ${overall_stats['lowest'][1]:.2f} (Category: {overall_stats['lowest'][0].title()}, Date: {overall_stats['lowest'][2]})")
print("\n=== UNIQUE CATEGORIES SPENT ON ===")
print(unique_categories)
print(f"Total unique categories: {len(unique_categories)}")
print("\n=== SPENDING BY CATEGORY ===")
for cat, sum in category_totals.items():
    print(f"{cat.title()}: ${sum:.2f}")