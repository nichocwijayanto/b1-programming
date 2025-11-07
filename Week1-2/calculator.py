#This program serves as a business calculator that calculates profit and protif margin percentage from revenue and cost data.

# Get revenue from user

revenue = input("Enter the total revenue: $")
    
if revenue.isdigit():
    revenue = float(revenue)
else:
    print("Invalid input for revenue. Please enter a numeric value.")

# Get costs from user
costs = input("Enter the total costs: $")

if costs.isdigit():
    costs = float(costs)
else:
    print("Invalid input for revenue. Please enter a numeric value.")

# Calculate profit and profit margin percentage
profit = revenue - costs
profit_margin_percentage = (profit / revenue) * 100

# Display results
print("\n---Financial Summary---")
print(f"Total Revenue: ${revenue:,.2f}")
print(f"Total Costs: ${costs:,.2f}")
print(f"Profit: ${profit:,.2f}")
print(f"Profit Margin Percentage: {profit_margin_percentage:.1f}%")