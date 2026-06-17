import pandas as pd
import sqlite3

# Read CSV
df = pd.read_csv("data/superstore.csv")

# Connect SQLite
conn = sqlite3.connect("database/sales.db")

# Load table
df.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Data loaded successfully!")