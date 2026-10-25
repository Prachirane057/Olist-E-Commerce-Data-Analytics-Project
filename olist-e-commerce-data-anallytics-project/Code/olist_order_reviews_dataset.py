
import pandas as pd
from pathlib import Path

# 1. File Paths

PROJECT = Path(
    r"D:\Data Analysis Protect 1\Olist-E-Commerce-Data-Analytics-Project"
)

RAW_PATH = PROJECT / "Raw Data" / "olist_order_reviews_dataset.csv"
ORDERS_PATH = PROJECT / "Raw Data" / "olist_orders_dataset.csv"
OUTPUT_PATH = PROJECT / "Cleaned Data" / "olist_order_reviews_dataset_cleaned.csv"


# 2. Read Data

if not RAW_PATH.exists():
    raise FileNotFoundError(f"Raw file not found: {RAW_PATH}")

df = pd.read_csv(RAW_PATH)

required_columns = [
    "review_id",
    "order_id",
    "review_score",
    "review_comment_title",
    "review_comment_message",
    "review_creation_date",
    "review_answer_timestamp"
]

missing_columns = set(required_columns) - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing expected columns: {missing_columns}")


# 3. Initial Audit

print("\nInitial Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nData Types:\n", df.dtypes)
print("\nFirst 5 Rows:\n", df.head())
print("\nMissing Values:\n", df.isna().sum())
print("\nMissing Percentages:\n", (df.isna().mean() * 100).round(2))
print("\nExact Duplicate Rows:", df.duplicated().sum())


# 4. Key Validation

print("\nUnique Review IDs:", df["review_id"].nunique())
print("Repeated Review ID Rows:", df["review_id"].duplicated().sum())
print("Unique Order IDs:", df["order_id"].nunique())
print("Repeated Order ID Rows:", df["order_id"].duplicated().sum())

print(
    "\nRepeated Review ID + Order ID Pairs:",
    df.duplicated(["review_id", "order_id"]).sum()
)

duplicate_review_ids = df[
    df["review_id"].duplicated(keep=False)
].sort_values("review_id")

print("\nRepeated Review ID Examples:\n", duplicate_review_ids.head(10))

duplicate_review_groups = df[
    df["review_id"].duplicated(keep=False)
]

non_order_columns = [
    col for col in df.columns if col != "order_id"
]

if not duplicate_review_groups.empty:
    group_attribute_counts = (
        duplicate_review_groups
        .groupby("review_id")[non_order_columns]
        .apply(lambda group: len(group.drop_duplicates()))
    )

    print(
        "\nRepeated Review IDs With Conflicting Attributes:",
        (group_attribute_counts > 1).sum()
    )


# 5. Review Score Validation

print("\nReview Score Counts:")
print(df["review_score"].value_counts(dropna=False).sort_index())

score_numeric = pd.to_numeric(df["review_score"], errors="coerce")

print(
    "\nScores Outside 1–5:",
    (~score_numeric.between(1, 5)).sum()
)


# 6. Text Audit

text_columns = [
    "review_id",
    "order_id",
    "review_comment_title",
    "review_comment_message"
]

for col in text_columns:
    values = df[col].dropna().astype(str)

    print(f"\n{col}")
    print("Leading/Trailing Spaces:", (values != values.str.strip()).sum())
    print("Whitespace-Only Values:", values.str.strip().eq("").sum())


# 7. Date Audit

date_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for col in date_columns:
    parsed = pd.to_datetime(df[col], errors="coerce")
    invalid = df[col].notna() & parsed.isna()

    print(f"\n{col}")
    print("Missing:", df[col].isna().sum())
    print("Invalid Dates:", invalid.sum())
    print("Minimum:", parsed.min())
    print("Maximum:", parsed.max())

creation_raw = pd.to_datetime(
    df["review_creation_date"], errors="coerce"
)

answer_raw = pd.to_datetime(
    df["review_answer_timestamp"], errors="coerce"
)

print(
    "\nAnswer Before Review Creation:",
    (answer_raw < creation_raw).sum()
)


# 8. Create Working Copy

clean_df = df.copy()


# 9. First-Pass Cleaning

clean_df["review_id"] = clean_df["review_id"].str.strip()
clean_df["order_id"] = clean_df["order_id"].str.strip()

score_before = clean_df["review_score"].copy()

clean_df["review_score"] = pd.to_numeric(
    clean_df["review_score"], errors="coerce"
)

invalid_score_conversion = (
    score_before.notna() & clean_df["review_score"].isna()
)

creation_before = clean_df["review_creation_date"].copy()

clean_df["review_creation_date"] = pd.to_datetime(
    clean_df["review_creation_date"], errors="coerce"
)

invalid_creation_conversion = (
    creation_before.notna()
    & clean_df["review_creation_date"].isna()
)

answer_before = clean_df["review_answer_timestamp"].copy()

clean_df["review_answer_timestamp"] = pd.to_datetime(
    clean_df["review_answer_timestamp"], errors="coerce"
)

invalid_answer_conversion = (
    answer_before.notna()
    & clean_df["review_answer_timestamp"].isna()
)

print("\nInvalid Score Conversions:", invalid_score_conversion.sum())
print("Invalid Creation-Date Conversions:", invalid_creation_conversion.sum())
print("Invalid Answer-Timestamp Conversions:", invalid_answer_conversion.sum())

print("\nTimestamp Data Types:")
print(clean_df[date_columns].dtypes)


# 10. Deferred Text Audit

for col in ["review_comment_title", "review_comment_message"]:
    values = clean_df[col].dropna().astype(str)

    print(f"\n{col} Before Second Pass")
    print("Whitespace-Only:", values.str.strip().eq("").sum())
    print("Surrounding Spaces:", (values != values.str.strip()).sum())


# 11. Second-Pass Cleaning

clean_df["review_comment_title"] = (
    clean_df["review_comment_title"].str.strip()
)

clean_df["review_comment_title"] = (
    clean_df["review_comment_title"].replace("", pd.NA)
)

clean_df["review_comment_message"] = (
    clean_df["review_comment_message"].str.strip()
)

clean_df["review_comment_message"] = (
    clean_df["review_comment_message"].replace("", pd.NA)
)


# 12. Final Validation

print("\nOriginal Shape:", df.shape)
print("Cleaned Shape:", clean_df.shape)
print("\nMissing Values:\n", clean_df.isna().sum())
print("\nExact Duplicate Rows:", clean_df.duplicated().sum())

print("Repeated Review IDs:", clean_df["review_id"].duplicated().sum())
print("Repeated Order IDs:", clean_df["order_id"].duplicated().sum())

print(
    "Repeated Review ID + Order ID Pairs:",
    clean_df.duplicated(["review_id", "order_id"]).sum()
)

print("\nReview Score Counts:")
print(clean_df["review_score"].value_counts(dropna=False).sort_index())

print("\nFinal Data Types:\n", clean_df.dtypes)

for col in ["review_id", "order_id"]:
    blank_ids = clean_df[col].isna() | clean_df[col].eq("")
    print(f"Missing/Blank {col}:", blank_ids.sum())

invalid_scores = (
    clean_df["review_score"].isna()
    | ~clean_df["review_score"].between(1, 5)
    | (clean_df["review_score"] % 1 != 0)
)

print("Missing or Invalid Scores:", invalid_scores.sum())

date_order_issues = (
    clean_df["review_answer_timestamp"]
    < clean_df["review_creation_date"]
)

print("Answer Before Creation:", date_order_issues.sum())

conversion_failures = (
    invalid_score_conversion.sum()
    + invalid_creation_conversion.sum()
    + invalid_answer_conversion.sum()
)

if conversion_failures:
    raise ValueError("Date or score conversion failures found.")

if invalid_scores.any():
    raise ValueError("Missing or invalid review scores found.")

if clean_df["review_id"].isna().any() or clean_df["order_id"].isna().any():
    raise ValueError("Missing review/order IDs found.")

for col in ["review_comment_title", "review_comment_message"]:
    values = clean_df[col].dropna().astype(str)

    print(f"\n{col} Final Check")
    print("Whitespace Remaining:", (values != values.str.strip()).sum())

print("\nFinal Timestamp Data Types:")
print(clean_df[date_columns].dtypes)


# 13. Cross-Table Validation

if ORDERS_PATH.exists():
    orders_df = pd.read_csv(ORDERS_PATH, usecols=["order_id"])

    known_order_ids = set(
        orders_df["order_id"].dropna().astype(str).str.strip()
    )

    review_order_ids = (
        clean_df["order_id"].dropna().astype(str).str.strip()
    )

    orphan_mask = ~review_order_ids.isin(known_order_ids)

    print(
        "\nReview Rows With Unknown Order IDs:",
        orphan_mask.sum()
    )

    if orphan_mask.any():
        print("Unmatched Order ID Examples:")
        print(review_order_ids[orphan_mask].head(10).tolist())
else:
    print("\nOrders file not found. Cross-table validation skipped.")


# 14. Save Cleaned Data

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

clean_df.to_csv(OUTPUT_PATH, index=False)


# 15. Verify Saved File

saved_df = pd.read_csv(OUTPUT_PATH)

print("\nSaved File:", OUTPUT_PATH)
print("Saved Shape:", saved_df.shape)
print("Expected Shape:", clean_df.shape)
print("Columns Match:", list(saved_df.columns) == list(clean_df.columns))
print("Saved Exact Duplicates:", saved_df.duplicated().sum())

if saved_df.shape != clean_df.shape:
    raise ValueError("Saved file shape mismatch.")

if list(saved_df.columns) != list(clean_df.columns):
    raise ValueError("Saved file columns mismatch.")

print("\nCleaning and verification completed successfully.")
