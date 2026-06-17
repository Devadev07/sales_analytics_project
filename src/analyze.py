import pandas as pd

# Load dataset
df = pd.read_csv("data/superstore.csv")

# KPIs
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()

print("\n===== SALES DASHBOARD KPIs =====")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Total Customers: {total_customers}")

print("\n===== TOP 10 PRODUCTS =====")

top_products = (
    df.groupby("Product Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print(top_products)

print("\n===== SALES BY REGION =====")

region_sales = (
    df.groupby("Region")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

print(region_sales)

df["Order Date"] = pd.to_datetime(df["Order Date"])

monthly_sales = (
    df.groupby(
        df["Order Date"].dt.to_period("M")
    )["Sales"]
    .sum()
)

print("\n===== MONTHLY SALES =====")
print(monthly_sales.tail())

print("\n===== TOP 10 CUSTOMERS =====")

top_customers = (
    df.groupby("Customer Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print(top_customers)

print("\n===== PROFIT BY CATEGORY =====")

category_profit = (
    df.groupby("Category")["Profit"]
      .sum()
      .sort_values(ascending=False)
)

print(category_profit)

print("\n===== DISCOUNT IMPACT =====")

discount_analysis = (
    df.groupby("Discount")[["Sales", "Profit"]]
      .mean()
      .round(2)
)

print(discount_analysis.head(10))

print("\n===== TOP PROFIT PRODUCTS =====")

top_profit_products = (
    df.groupby("Product Name")["Profit"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print(top_profit_products)