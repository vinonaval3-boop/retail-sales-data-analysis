import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("superstore.csv", encoding="latin1")

# Remove missing values
df.dropna(inplace=True)

# Convert Order Date column
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Create Month column
df["Month"] = df["Order Date"].dt.to_period("M")

# Monthly Sales
monthly_sales = df.groupby("Month")["Sales"].sum()

print("Monthly Sales:")
print(monthly_sales.head())

# Top 5 Products
top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(5)

print("\nTop 5 Products:")
print(top_products)

# Plot
monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("monthly_sales.png")
plt.show()

# SQLite Database
conn = sqlite3.connect("sales.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

query = """
SELECT Category, SUM(Sales) as Total_Sales
FROM sales
GROUP BY Category
ORDER BY Total_Sales DESC
"""

result = pd.read_sql(query, conn)

print("\nCategory-wise Sales:")
print(result)

conn.close()