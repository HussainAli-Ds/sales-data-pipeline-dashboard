WATCH_FOLDER = r"C:\project\input_files"
PROCESSED_FOLDER = r"C:\project\processed_files"
FAILED_FOLDER = r"C:\project\failed_files"
LOG_FILE = "logs/pipeline.log"

DB_URI = "postgresql+psycopg2://username:password@localhost:5432/database_name"

EXPECTED_COLUMNS = [
    "Sale Date", "Customer Name", "City", "State",
    "Region", "Product Category", "Product Name",
    "Quantity", "Price per Unit", "Sales Amount"
]

RENAMED_COLUMNS = [
    "SALE_DATE", "CUSTOMER_NAME", "CITY", "STATE_ORDER",
    "REGION", "PRODUCT_CATEGORY", "PRODUCT_NAME",
    "QUANTITY", "PRICE_PER_UNIT", "SALES_AMOUNT"
]