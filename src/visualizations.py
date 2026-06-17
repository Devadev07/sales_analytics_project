import pandas as pd
import matplotlib.pyplot as plt

# Load the CLEANED dataset (run src/clean_data.py first to generate it)
df = pd.read_csv("data/superstore_clean.csv", parse_dates=["Order Date", "Ship Date"])

# Monthly Sales
monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
      .sum()
)

plt.figure(figsize=(12,6))
monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("charts/monthly_sales.png")
plt.close()

# Top Products
top_products = (
    df.groupby("Product Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

plt.figure(figsize=(12,6))
top_products.sort_values().plot(kind="barh")
plt.title("Top 10 Products by Revenue")
plt.tight_layout()
plt.savefig("charts/top_products.png")
plt.close()

# Region Sales
region_sales = (
    df.groupby("Region")["Sales"]
      .sum()
      .sort_values()
)

plt.figure(figsize=(8,5))
region_sales.plot(kind="bar")
plt.title("Revenue by Region")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("charts/region_sales.png")
plt.close()

print("Charts generated successfully!")