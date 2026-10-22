import pandas as pd

# STEP 1: LOADING DATASET
df = pd.read_csv(
    r"D:\Data Analysis Protect 1\Olist-E-Commerce-Data-Analytics-Project\Raw Data\olist_orders_dataset.csv"
)

print("Dataset loaded successfully.")


# STEP 2: INITIAL DATA INSPECTION

print("\n INITIAL DATA INSPECTION ")

print("\nDataset Shape:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nFirst 5 Rows:")
print(df.head())

print("\nLast 5 Rows:")
print(df.tail())


# STEP 3: CHECKING MISSING VALUES

missing_values = df.isna().sum()
missing_values_percentages = (df.isna().mean() * 100).round(2)

missing_report = pd.DataFrame({
    "missing_values": missing_values,
    "missing_values_percentages": missing_values_percentages
})

print("\nMissing Value Report:")
print(missing_report)


# STEP 4: CHECKING DUPLICATE ROWS

duplicated_values = df.duplicated().sum()

duplicated_values_percentages = (
    df.duplicated().mean() * 100
).round(2)

print("\nDuplicated Rows:", duplicated_values)
print("Duplicated Rows Percentage:", duplicated_values_percentages)

duplicate_rows = df[df.duplicated(keep=False)]

print("\nRecords with Exact Duplicate Rows:")
print(duplicate_rows)


# STEP 5: CHECKING UNIQUE AND DUPLICATE IDs

total_records = len(df)

unique_order_ids = df["order_id"].nunique()
duplicated_order_ids = df["order_id"].duplicated().sum()

unique_customer_ids = df["customer_id"].nunique()
duplicated_customer_ids = df["customer_id"].duplicated().sum()

print("\nTotal Records:", total_records)

print("\nUnique Order IDs:", unique_order_ids)
print("Duplicated Order IDs:", duplicated_order_ids)

print("\nUnique Customer IDs:", unique_customer_ids)
print("Repeated Customer IDs:", duplicated_customer_ids)

duplicate_order_records = df[
    df["order_id"].duplicated(keep=False)
].sort_values("order_id")

print("\nRecords with Duplicate Order IDs:")
print(duplicate_order_records)


# STEP 6: CHECKING ORDER STATUS

print("\nDistinct Order Statuses:")
print(sorted(df["order_status"].dropna().unique()))

print("\nOrder Status Counts:")
print(df["order_status"].value_counts(dropna=False))


# STEP 7: CHECKING EXTRA WHITE SPACES

text_cols = ["order_id", "customer_id", "order_status"]

print("\nChecking Extra White Spaces:")

for col in text_cols:
    whitespace_mask = (
        df[col].notna()
        & df[col].ne(df[col].str.strip())
    )

    print(f"{col}: {whitespace_mask.sum()} values with extra whitespace")


# STEP 8: CHECKING DATE FORMAT

date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

print("\nChecking Date Formats:")

for col in date_cols:
    parsed_dates = pd.to_datetime(df[col], errors="coerce")

    invalid_dates = (
        df[col].notna()
        & parsed_dates.isna()
    )

    print(f"\n{col}")
    print("Missing Values:", df[col].isna().sum())
    print("Invalid Date Values:", invalid_dates.sum())


# ==================================================
# STEP 9: CREATING A SEPARATE CLEANED DATASET
# ==================================================

clean_df = df.copy()

print("\nSeparate cleaning DataFrame created.")


# STEP 10: APPLYING CLEANING CHANGES

# Removing Extra White Spaces
for col in text_cols:
    clean_df[col] = clean_df[col].str.strip()

# Converting Date Columns to Datetime
# Missing dates will remain NaT.
# No dates will be filled with averages or guesses.

for col in date_cols:
    clean_df[col] = pd.to_datetime(
        clean_df[col],
        errors="coerce"
    )

print("\nBasic cleaning changes applied.")


# STEP 11: CHECKING LOGICAL DATE SEQUENCES

# Purchase should not be after approval
purchase_after_approval = (
    clean_df["order_purchase_timestamp"].notna()
    & clean_df["order_approved_at"].notna()
    & (
        clean_df["order_purchase_timestamp"]
        > clean_df["order_approved_at"]
    )
)

# Carrier handover before purchase
carrier_before_purchase = (
    clean_df["order_delivered_carrier_date"].notna()
    & clean_df["order_purchase_timestamp"].notna()
    & (
        clean_df["order_delivered_carrier_date"]
        < clean_df["order_purchase_timestamp"]
    )
)

# Carrier handover after customer delivery
carrier_after_delivery = (
    clean_df["order_delivered_carrier_date"].notna()
    & clean_df["order_delivered_customer_date"].notna()
    & (
        clean_df["order_delivered_carrier_date"]
        > clean_df["order_delivered_customer_date"]
    )
)

# Customer delivery before purchase
delivery_before_purchase = (
    clean_df["order_delivered_customer_date"].notna()
    & clean_df["order_purchase_timestamp"].notna()
    & (
        clean_df["order_delivered_customer_date"]
        < clean_df["order_purchase_timestamp"]
    )
)

print("\n========== DATE SEQUENCE VALIDATION ==========")

print("Purchase After Approval:", purchase_after_approval.sum())
print("Carrier Before Purchase:", carrier_before_purchase.sum())
print("Carrier After Customer Delivery:", carrier_after_delivery.sum())
print("Customer Delivery Before Purchase:", delivery_before_purchase.sum())


# Displaying Suspicious Timestamp Records
suspicious_mask = (
    purchase_after_approval
    | carrier_before_purchase
    | carrier_after_delivery
    | delivery_before_purchase
)

suspicious_cols = [
    "order_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

print("\nSuspicious Timestamp Records:")
print(clean_df.loc[suspicious_mask, suspicious_cols])


# STEP 12: CHECKING MISSING DATES BY ORDER STATUS

date_check_cols = [
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date"
]

missing_by_status = clean_df.groupby("order_status")[
    date_check_cols
].agg(lambda col: col.isna().sum())

print("\nMissing Dates by Order Status:")
print(missing_by_status)


# STEP 13: FINAL RECHECK

print("\n========== FINAL RECHECK ==========")

print("Original Rows:", len(df))
print("Cleaned Rows:", len(clean_df))
print("Rows Removed:", len(df) - len(clean_df))

print("\nFinal Dataset Shape:")
print(clean_df.shape)

print("\nFinal Data Types:")
print(clean_df.dtypes)

print("\nFinal Missing Values:")
print(clean_df.isna().sum())

print("\nFinal Exact Duplicate Rows:")
print(clean_df.duplicated().sum())

print(
    "\nFinal Duplicate Order IDs:",
    clean_df["order_id"].duplicated().sum()
)

print("\nFinal Order Statuses:")
print(sorted(clean_df["order_status"].dropna().unique()))

print("\nFinal Date-Time Data Types:")
print(clean_df[date_cols].dtypes)

print("\nFinal First 5 Rows:")
print(clean_df.head())

print("\nFinal Last 5 Rows:")
print(clean_df.tail())

print("\nFinal Dataset Information:")
clean_df.info()


# STEP 14: SAVING CLEANED DATASET

clean_df.to_csv(
    r"D:\Data Analysis Protect 1\Olist-E-Commerce-Data-Analytics-Project\Cleaned Data\olist_orders_dataset_cleaned.csv",
    index=False
)

print("\nCleaned dataset saved successfully.")