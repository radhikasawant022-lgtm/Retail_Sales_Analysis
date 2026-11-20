"""
Retail Sales Analysis
Run: python retail_sales_analysis.py
Input: retail_sales_data.csv
Outputs: category_summary.csv, monthly_summary.csv, city_summary.csv
"""
import pandas as pd

df = pd.read_csv("retail_sales_data.csv", parse_dates=["Order_Date"])

# Basic data quality checks
print("Rows:", len(df))
print("Missing values:\n", df.isna().sum())
print("Duplicate order IDs:", df["Order_ID"].duplicated().sum())

# Key performance indicators
total_revenue = df["Revenue_INR"].sum()
total_profit = df["Profit_INR"].sum()
total_orders = df["Order_ID"].nunique()
total_units = df["Quantity"].sum()
avg_order_value = total_revenue / total_orders
profit_margin = total_profit / total_revenue * 100

print("\nKEY PERFORMANCE INDICATORS")
print(f"Total orders: {total_orders:,}")
print(f"Units sold: {total_units:,}")
print(f"Revenue: ₹{total_revenue:,.2f}")
print(f"Profit: ₹{total_profit:,.2f}")
print(f"Average order value: ₹{avg_order_value:,.2f}")
print(f"Profit margin: {profit_margin:.2f}%")

# Business analysis
category_summary = df.groupby("Category", as_index=False).agg(
    Revenue_INR=("Revenue_INR", "sum"),
    Profit_INR=("Profit_INR", "sum"),
    Units_Sold=("Quantity", "sum")
).sort_values("Revenue_INR", ascending=False)

monthly_summary = df.assign(
    Month=df["Order_Date"].dt.to_period("M").astype(str)
).groupby("Month", as_index=False).agg(
    Revenue_INR=("Revenue_INR", "sum"),
    Profit_INR=("Profit_INR", "sum")
)

city_summary = df.groupby("City", as_index=False).agg(
    Revenue_INR=("Revenue_INR", "sum"),
    Profit_INR=("Profit_INR", "sum"),
    Orders=("Order_ID", "nunique")
).sort_values("Revenue_INR", ascending=False)

category_summary.to_csv("category_summary.csv", index=False)
monthly_summary.to_csv("monthly_summary.csv", index=False)
city_summary.to_csv("city_summary.csv", index=False)

print("\nTop category by revenue:", category_summary.iloc[0]["Category"])
print("Top city by revenue:", city_summary.iloc[0]["City"])
print("\nAnalysis complete. Summary CSV files created.")
