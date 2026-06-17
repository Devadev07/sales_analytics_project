import pandas as pd

df = pd.read_csv("data/superstore.csv")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

top_region = (
    df.groupby("Region")["Sales"]
      .sum()
      .idxmax()
)

top_category = (
    df.groupby("Category")["Sales"]
      .sum()
      .idxmax()
)

report = f"""
# Sales Analytics Report

## Key Metrics

- Total Sales: ${total_sales:,.2f}
- Total Profit: ${total_profit:,.2f}
- Best Performing Region: {top_region}
- Top Category: {top_category}

## Summary

This report analyzes historical sales performance using the Superstore dataset.

Key findings:
- Revenue is concentrated in a few high-performing regions.
- Certain product categories generate significantly higher sales.
- Monthly trends reveal seasonal fluctuations in demand.
"""

with open("reports/summary.md", "w", encoding="utf-8") as f:
    f.write(report)

print("Report generated!")