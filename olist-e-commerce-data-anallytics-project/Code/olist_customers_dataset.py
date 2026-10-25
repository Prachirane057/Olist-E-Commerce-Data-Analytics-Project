import pandas as pd

# Loading Dataset
df = pd.read_csv(
    r"C:\Users\Mayank Ganeshe\Documents\Clean Data\olist_customers_dataset.csv"
)

# STEP 1: INITIAL DATA INSPECTION
print("Dataset shape:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

# Checking Missing Values
missing_values = df.isna().sum()
missing_values_percentages = (df.isna().mean() * 100).round(2)

missing_report = pd.DataFrame({
    "missing_values": missing_values,
    "missing_values_percentages": missing_values_percentages
})

print("\nMissing Value Report:")
print(missing_report)

# Checking Duplicate Rows
duplicated_values = df.duplicated().sum()
duplicated_values_percentages = (df.duplicated().mean() * 100).round(2)

print("\nDuplicated Rows:", duplicated_values)
print("Duplicated Rows Percentage:", duplicated_values_percentages)

duplicate_rows = df[df.duplicated(keep=False)]

print("\nRecords with Exact Duplicate Rows:")
print(duplicate_rows)

# Checking Duplicate customer_id
total_records = len(df)
unique_customer_ids = df["customer_id"].nunique()
duplicated_customer_ids = df["customer_id"].duplicated().sum()

print("\nTotal Records:", total_records)
print("Unique Customer IDs:", unique_customer_ids)
print("Duplicated Customer IDs:", duplicated_customer_ids)

duplicated_customer_ids_names = df[
    df["customer_id"].duplicated(keep=False)
].sort_values("customer_id")

print("\nRecords with Duplicated Customer IDs:")
print(duplicated_customer_ids_names)

# Checking Unique Customer Identities
print("\nUnique customer IDs:", df["customer_id"].nunique())
print("Unique customer identities:", df["customer_unique_id"].nunique())
print("Missing customer identities:", df["customer_unique_id"].isna().sum())


# STEP 2: INSPECTING DATA QUALITY PROBLEMS

# Checking ZIP Prefixes
zip_prefix = df["customer_zip_code_prefix"].astype("string").str.strip()

zip_mask = (
    zip_prefix.str.len().ne(5)
    & zip_prefix.notna()
)

print("\nZIP Prefixes with Unexpected Length:", zip_mask.sum())

print("\nProblematic ZIP Prefix Records:")
print(
    df.loc[
        zip_mask,
        ["customer_id", "customer_zip_code_prefix"]
    ]
)

# Checking Extra White Spaces
print("\nChecking Extra White Spaces:")

for col in ["customer_city", "customer_state"]:
    whitespace_mask = (
        df[col].notna()
        & df[col].ne(df[col].str.strip())
    )

    print(f"{col}: {whitespace_mask.sum()} values with extra whitespace")

# Validating State Codes
print("\nDistinct Customer State Codes:")
print(sorted(df["customer_state"].dropna().unique()))


# STEP 3: CREATING A SEPARATE CLEANING DATAFRAME

# Original df will remain unchanged
clean_df = df.copy()

# Removing the last row ONLY if it has been confirmed
# to be an unwanted, entirely empty row.
if clean_df.iloc[-1].isna().all():
    clean_df = clean_df.iloc[:-1].copy()
    print("\nRemoved the last row because it was entirely empty.")
else:
    print("\nLast row is not entirely empty. No row removed.")


# STEP 4: APPLYING CONFIRMED CLEANING CHANGES

# Converting ZIP Prefixes to Strings
# This preserves leading zeros if present.
clean_df["customer_zip_code_prefix"] = (
    clean_df["customer_zip_code_prefix"]
    .astype("string")
    .str.strip()
)

# Removing Extra White Spaces from City and State
for col in ["customer_city", "customer_state"]:
    clean_df[col] = clean_df[col].str.strip()

# Do not replace unknown state codes without verification.
# Do not delete duplicate IDs without investigating them.


# STEP 5: FINAL DATA RECHECK

print("\n========== FINAL RECHECK ==========")

print("\nOriginal Rows:", len(df))
print("Cleaned Rows:", len(clean_df))
print("Rows Removed:", len(df) - len(clean_df))

print("\nFinal Dataset Shape:", clean_df.shape)

print("\nFinal Data Types:")
print(clean_df.dtypes)

print("\nFinal Missing Value Report:")
print(clean_df.isna().sum())

print("\nFinal Exact Duplicate Rows:", clean_df.duplicated().sum())

print(
    "\nCustomer ID Duplicates:",
    clean_df["customer_id"].duplicated().sum()
)

print(
    "Unique Customer IDs:",
    clean_df["customer_id"].nunique()
)

print(
    "Unique Customer Identities:",
    clean_df["customer_unique_id"].nunique()
)

print(
    "Missing Customer Identities:",
    clean_df["customer_unique_id"].isna().sum()
)

# Rechecking ZIP Prefix Length
final_zip_mask = (
    clean_df["customer_zip_code_prefix"].str.len().ne(5)
    & clean_df["customer_zip_code_prefix"].notna()
)

print("\nFinal ZIP Prefixes with Unexpected Length:", final_zip_mask.sum())

# Rechecking White Spaces
print("\nFinal Extra White Space Check:")

for col in ["customer_city", "customer_state"]:
    whitespace_mask = (
        clean_df[col].notna()
        & clean_df[col].ne(clean_df[col].str.strip())
    )

    print(f"{col}: {whitespace_mask.sum()} values with extra whitespace")

# Final State Code Check
valid_states = {
    "AC", "AL", "AP", "AM", "BA", "CE", "DF",
    "ES", "GO", "MA", "MT", "MS", "MG", "PA",
    "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
    "RO", "RR", "SC", "SP", "SE", "TO"
}

found_states = set(clean_df["customer_state"].dropna().unique())
unexpected_states = found_states - valid_states

print("\nFinal Distinct State Codes:", sorted(found_states))
print("Unexpected State Codes:", sorted(unexpected_states))


# STEP 6: DISPLAY FINAL CLEANED DATA

print("\n========== FINAL CLEANED DATA ==========")

print("\nFirst 5 Rows:")
print(clean_df.head())

print("\nLast 5 Rows:")
print(clean_df.tail())

print("\nFinal Dataset Information:")
clean_df.info()


# STEP 7: SAVING CLEANED DATASET

clean_df.to_csv(
    r"C:\Users\Mayank Ganeshe\Documents\Clean Data\olist_customers_dataset_cleaned.csv",
    index=False
)

print("\nCleaned dataset saved successfully.")
