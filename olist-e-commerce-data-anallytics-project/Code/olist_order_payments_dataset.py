import pandas as pd
from pathlib import Path

# File paths
RAW_PATH = Path(
    r"D:\Data Analysis Protect 1\Olist-E-Commerce-Data-Analytics-Project"
    r"\Raw Data\olist_order_payments_dataset.csv"
)

OUTPUT_PATH = Path(
    r"D:\Data Analysis Protect 1\Olist-E-Commerce-Data-Analytics-Project"
    r"\Cleaned Data\olist_order_payments_dataset_cleaned.csv"
)

#READ RAW DATA

if not RAW_PATH.exists():
    raise FileNotFoundError(f"Raw file not found: {RAW_PATH}")

df = pd.read_csv(RAW_PATH)

print("\nShape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())
print("\nData types:")
print(df.dtypes)


#INITIAL QUALITY CHECKS

print("\nMissing values:")
print(df.isna().sum())

print("\nMissing value percentages:")
print((df.isna().mean() * 100).round(2))

print("\nExact duplicate rows:", df.duplicated().sum())

print("\nUnique order IDs:", df["order_id"].nunique())

print("\nDuplicate order IDs:")
print(df["order_id"].duplicated().sum())

# Duplicate order_id + payment_sequential combinations check
print("\nDuplicate order_id + payment_sequential combinations:")
print(
    df.duplicated(
        subset=["order_id", "payment_sequential"]
    ).sum()
)

print("\nPayment type counts:")
print(df["payment_type"].value_counts(dropna=False))

print("\nPayment sequential counts:")
print(df["payment_sequential"].value_counts(dropna=False).sort_index())

print("\nPayment installment counts:")
print(
    df["payment_installments"]
    .value_counts(dropna=False)
    .sort_index()
)

print("\nPayment value summary:")
print(df["payment_value"].describe())

# Check suspicious numeric values BEFORE making changes.
print("\nNegative payment values:")
print((df["payment_value"] < 0).sum())

print("\nZero payment values:")
print((df["payment_value"] == 0).sum())

print("\nPayment installments below 1:")
print((df["payment_installments"] < 1).sum())

print("\nPayment sequential values below 1:")
print((df["payment_sequential"] < 1).sum())

#CREATE A WORKING COPY

# Work on a copy so that the original raw DataFrame stays unchanged.

clean_df = df.copy()

#FIRST-PASS CLEANING
# Each change is performed separately and documented.

# Remove leading/trailing spaces from order_id.
# Do not modify the actual ID values beyond whitespace.

clean_df["order_id"] = clean_df["order_id"].str.strip()

# Remove leading/trailing spaces from payment_type.
# Do not rename payment categories without a justified rule.

clean_df["payment_type"] = clean_df["payment_type"].str.strip()

# Invalid values become missing and are reported below.

original_sequential = clean_df["payment_sequential"].copy()

clean_df["payment_sequential"] = pd.to_numeric(
    clean_df["payment_sequential"],
    errors="coerce"
)

invalid_sequential = (
    original_sequential.notna()
    & clean_df["payment_sequential"].isna()
)

print("\nInvalid payment_sequential conversions:", invalid_sequential.sum())

# Convert payment_installments to numeric.
# Do not guess or fill missing installment counts.

original_installments = clean_df["payment_installments"].copy()

clean_df["payment_installments"] = pd.to_numeric(
    clean_df["payment_installments"],
    errors="coerce"
)

invalid_installments = (
    original_installments.notna()
    & clean_df["payment_installments"].isna()
)

print("Invalid payment_installments conversions:", invalid_installments.sum())

# INTENTIONALLY DEFERRED CHECK

# payment_value conversion and validation are intentionally
# left for the second pass.
#
# This lets us audit the original values first.
# We are NOT deleting rows or filling missing payment values.


print("\npayment_value data type BEFORE second pass:")
print(clean_df["payment_value"].dtype)

print("\nSample payment_value values BEFORE second pass:")
print(clean_df["payment_value"].head(10).tolist())

# Resolve the deferred numeric validation.

# Convert payment_value to numeric and report any conversion
# failures. No values are filled with averages or guesses.

original_payment_value = clean_df["payment_value"].copy()

clean_df["payment_value"] = pd.to_numeric(
    clean_df["payment_value"],
    errors="coerce"
)

invalid_payment_value = (
    original_payment_value.notna()
    & clean_df["payment_value"].isna()
)

print("\nInvalid payment_value conversions:", invalid_payment_value.sum())

# If any non-missing source values became missing during
# numeric conversion, stop before saving so the issue can
# be investigated rather than silently losing information.

if (
    invalid_sequential.sum() > 0
    or invalid_installments.sum() > 0
    or invalid_payment_value.sum() > 0
):
    raise ValueError(
        "Some non-missing values failed numeric conversion. "
        "Review the reported source values before saving."
    )

#VALIDATION AFTER ALL CHANGES


print("\nOriginal shape:", df.shape)
print("Cleaned shape:", clean_df.shape)

print("\nMissing values after cleaning:")
print(clean_df.isna().sum())

print("\nExact duplicate rows after cleaning:")
print(clean_df.duplicated().sum())

print("\nDuplicate order_id + payment_sequential combinations:")
print(
    clean_df.duplicated(
        subset=["order_id", "payment_sequential"]
    ).sum()
)

print("\nUnique order IDs after cleaning:")
print(clean_df["order_id"].nunique())

print("\nPayment types after cleaning:")
print(clean_df["payment_type"].value_counts(dropna=False))

print("\nFinal data types:")
print(clean_df.dtypes)

print("\nFinal payment_value summary:")
print(clean_df["payment_value"].describe())

# Recheck suspicious values. Report them; do not automatically
# delete them because they need business-context investigation.

print("\nNegative payment values after cleaning:")
print((clean_df["payment_value"] < 0).sum())

print("\nZero payment values after cleaning:")
print((clean_df["payment_value"] == 0).sum())

print("\nInstallments below 1 after cleaning:")
print((clean_df["payment_installments"] < 1).sum())

print("\nSequential values below 1 after cleaning:")
print((clean_df["payment_sequential"] < 1).sum())

#SAVE ONCE, AFTER ALL CHANGES AND RECHECKS

# Create the output directory if it does not exist.

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# Save the completed cleaned DataFrame only once.
# The original raw CSV is never overwritten.

clean_df.to_csv(OUTPUT_PATH, index=False)

print("Cleaned file saved at:")
print(OUTPUT_PATH)

print("\nOriginal raw file preserved:")
print(RAW_PATH)
