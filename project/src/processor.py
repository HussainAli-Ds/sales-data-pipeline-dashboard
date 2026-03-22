import pandas as pd
import logging
from config import EXPECTED_COLUMNS, RENAMED_COLUMNS
from db import insert_data

def process_file(file_path):
    try:
        logging.info(f"Processing: {file_path}")

        df = pd.read_excel(file_path)

        # Validate headers
        if list(df.columns) != EXPECTED_COLUMNS:
            raise ValueError("Column mismatch")

        df.columns = RENAMED_COLUMNS
        df.columns = [col.lower() for col in df.columns]
        # Convert date
        df["sale_date"] = pd.to_datetime(
            df["sale_date"], origin="1899-12-30", unit="D"
        )

        # Clean
        df["customer_name"] = df["customer_name"].fillna("Unknown")
        df["city"] = df["city"].fillna("No-City")

        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df["price_per_unit"] = pd.to_numeric(df["price_per_unit"], errors="coerce")
        df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce")

        df.dropna(inplace=True)

        df = df[
            (df["quantity"] > 0) &
            (df["price_per_unit"] > 0) &
            (df["sales_amount"] > 0)
        ]

        # Remove duplicates (file level)
        df.drop_duplicates(
            subset=["sale_date", "customer_name", "product_name", "city"],
            inplace=True
        )

        if df.empty:
            raise ValueError("No valid data")

        insert_data(df)

        logging.info(f"Inserted {len(df)} rows")
        return True

    except Exception as e:
        print("PROCESS ERROR:", str(e))   # 👈 ADD THIS
        logging.error(str(e))
        return False