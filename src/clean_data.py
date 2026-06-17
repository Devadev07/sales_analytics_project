"""
clean_data.py
-------------
Cleans the raw Superstore CSV and produces:
  1. data/superstore_clean.csv  -> Power BI / BI-tool ready file
  2. database/sales.db (table: sales_clean) -> for SQL queries

The raw export has real data-quality issues that this script fixes:
  - 806 blank/null rows
  - 504 fully duplicated rows
  - 799 duplicate Row IDs
  - Order/Ship dates stored as inconsistent M/D/Y strings
  - Numeric columns loaded as floats

Run from the project root:
    python src/clean_data.py
"""

import os
import sqlite3

import numpy as np
import pandas as pd

RAW_PATH = "data/superstore.csv"
CLEAN_CSV_PATH = "data/superstore_clean.csv"
DB_PATH = "database/sales.db"


def load_raw(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded raw data: {df.shape[0]:,} rows, {df.shape[1]} columns")
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    start_rows = len(df)

    # 1. Drop rows missing any key business field.
    #    In this export, ~806 rows are blank placeholders (no Sales/Date/Profit).
    key_cols = ["Order Date", "Sales", "Profit", "Quantity"]
    df = df.dropna(subset=key_cols, how="any")
    after_nulls = len(df)
    print(f"Removed {start_rows - after_nulls:,} blank/null rows")

    # 2. Remove fully duplicated rows.
    df = df.drop_duplicates()
    after_dupes = len(df)
    print(f"Removed {after_nulls - after_dupes:,} fully duplicate rows")

    # 3. Remove duplicate Row IDs (each transaction line should be unique).
    df = df.drop_duplicates(subset=["Row ID"], keep="first")
    after_rowid = len(df)
    print(f"Removed {after_dupes - after_rowid:,} duplicate Row IDs")

    # 4. Parse dates (source format is month-first M/D/Y).
    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce", dayfirst=False, format="mixed"
    )
    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"], errors="coerce", dayfirst=False, format="mixed"
    )
    df = df.dropna(subset=["Order Date"])
    print(f"Parsed dates -> range {df['Order Date'].min():%Y-%m-%d} "
          f"to {df['Order Date'].max():%Y-%m-%d}")

    # 5. Fix numeric / id types.
    df["Quantity"] = df["Quantity"].astype(int)
    df["Postal Code"] = df["Postal Code"].astype("Int64")  # nullable integer
    for col in ["Sales", "Profit", "Discount"]:
        df[col] = df[col].round(2)

    # 6. Derived analytics columns.
    df["Profit Margin"] = np.where(
        df["Sales"] != 0, (df["Profit"] / df["Sales"]).round(4), 0
    )
    df["Order Year"] = df["Order Date"].dt.year
    df["Order Month"] = df["Order Date"].dt.month
    df["Order Month Name"] = df["Order Date"].dt.strftime("%Y-%m")
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # 7. Strip stray whitespace from text fields.
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        df[col] = df[col].str.strip()

    df = df.reset_index(drop=True)
    print(f"Final clean dataset: {len(df):,} rows "
          f"({start_rows - len(df):,} removed total)")
    return df


def export_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
    print(f"Wrote clean CSV -> {path}")


def load_to_sqlite(df: pd.DataFrame, db_path: str) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    # Store dates as ISO strings so SQLite date functions work.
    out = df.copy()
    out["Order Date"] = out["Order Date"].dt.strftime("%Y-%m-%d")
    out["Ship Date"] = out["Ship Date"].dt.strftime("%Y-%m-%d")
    out.to_sql("sales_clean", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Loaded table 'sales_clean' -> {db_path}")


def main() -> None:
    print("===== CLEANING SUPERSTORE DATA =====")
    df = load_raw(RAW_PATH)
    df = clean(df)
    export_csv(df, CLEAN_CSV_PATH)
    load_to_sqlite(df, DB_PATH)
    print("===== DONE =====")


if __name__ == "__main__":
    main()
