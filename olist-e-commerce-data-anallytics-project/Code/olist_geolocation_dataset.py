
from pathlib import Path
import unicodedata
import pandas as pd

# 1. FILE PATHS

PROJECT_DIR = Path(
    r"D:\Data Analysis Protect 1\Olist-E-Commerce-Data-Analytics-Project"
)

RAW_PATH = PROJECT_DIR / "Raw Data" / "olist_geolocation_dataset.csv"

OUTPUT_PATH = (
    PROJECT_DIR
    / "Cleaned Data"
    / "olist_geolocation_dataset_cleaned.csv"
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# 2. LOAD RAW DATA

try:
    df = pd.read_csv(
        RAW_PATH,
        dtype={
            "geolocation_zip_code_prefix": "string",
            "geolocation_city": "string",
            "geolocation_state": "string",
        },
        encoding="utf-8-sig",
    )

except UnicodeDecodeError:
    # Fallback only if UTF-8 decoding fails.
    df = pd.read_csv(
        RAW_PATH,
        dtype={
            "geolocation_zip_code_prefix": "string",
            "geolocation_city": "string",
            "geolocation_state": "string",
        },
        encoding="cp1252",
    )


required_columns = [
    "geolocation_zip_code_prefix",
    "geolocation_lat",
    "geolocation_lng",
    "geolocation_city",
    "geolocation_state",
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns missing: {missing_columns}"
    )


# 3. INITIAL AUDIT

print("\n========== INITIAL AUDIT ==========")

print("Original shape:", df.shape)
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n", df.isna().sum())
print("\nExact duplicate rows:", df.duplicated().sum())

print(
    "\nUnique ZIP prefixes:",
    df["geolocation_zip_code_prefix"].nunique()
)

print(
    "Unique city values:",
    df["geolocation_city"].nunique()
)

print(
    "Unique state values:",
    df["geolocation_state"].nunique()
)

print("\nOriginal city examples:")
print(df["geolocation_city"].value_counts().head(15))


# 4. CREATE A WORKING COPY

clean_df = df.copy()


# 5. CLEAN ZIP CODE PREFIXES

zip_col = "geolocation_zip_code_prefix"

clean_df[zip_col] = clean_df[zip_col].str.strip()

# Keep only numeric prefixes of 1 to 5 digits for standardizing.
valid_zip_format = clean_df[zip_col].str.fullmatch(
    r"\d{1,5}", na=False
)

clean_df.loc[valid_zip_format, zip_col] = (
    clean_df.loc[valid_zip_format, zip_col].str.zfill(5)
)

# Do not silently delete malformed ZIP prefixes.
invalid_zip = ~clean_df[zip_col].str.fullmatch(
    r"\d{5}", na=False
)


# 6. CONVERT COORDINATES TO NUMERIC

clean_df["geolocation_lat"] = pd.to_numeric(
    clean_df["geolocation_lat"],
    errors="coerce",
)

clean_df["geolocation_lng"] = pd.to_numeric(
    clean_df["geolocation_lng"],
    errors="coerce",
)


# 7. REPAIR POSSIBLE MOJIBAKE IN CITY NAMES

def repair_mojibake(value):
    """
    Attempts to repair common UTF-8 text read incorrectly
    as a single-byte encoding.
    """

    if pd.isna(value):
        return value

    value = str(value).strip()

    # Attempt repair only when common corruption markers occur.
    if "Ã" in value or "Â" in value:
        try:
            repaired = value.encode("latin1").decode("utf-8")
            return repaired
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

    return value


# 8. NORMALIZE CITY NAMES CONSISTENTLY

def normalize_city(value):
    """
    City normalization policy:
    - Repair common mojibake where possible.
    - Remove leading/trailing and repeated whitespace.
    - Convert to lowercase.
    - Remove accents consistently.

    Examples:
    'são paulo'  -> 'sao paulo'
    'sao paulo'  -> 'sao paulo'
    'sÃ£o paulo' -> 'sao paulo' when repairable
    """

    if pd.isna(value):
        return pd.NA

    value = repair_mojibake(value)
    value = " ".join(str(value).strip().lower().split())

    # Unicode decomposition separates letters from accent marks.
    value = unicodedata.normalize("NFKD", value)

    # Remove accent marks, keeping the base letters.
    value = "".join(
        char for char in value
        if not unicodedata.combining(char)
    )

    return value if value else pd.NA


city_col = "geolocation_city"
state_col = "geolocation_state"

# Save original city values in memory for before/after comparison.
original_city = clean_df[city_col].copy()

clean_df[city_col] = clean_df[city_col].apply(normalize_city)


print(
    "Unique city values before:",
    original_city.nunique()
)

print(
    "Unique city values after:",
    clean_df[city_col].nunique()
)

print("\nMost common cleaned city values:")
print(clean_df[city_col].value_counts().head(15))

print(
    "\nSão Paulo standardized value count:",
    clean_df[city_col].eq("sao paulo").sum()
)


# 9. NORMALIZE STATE CODES

clean_df[state_col] = (
    clean_df[state_col]
    .str.strip()
    .str.upper()
)

clean_df[state_col] = clean_df[state_col].replace(
    "", pd.NA
)

# Clean blank ZIP strings too.
clean_df[zip_col] = clean_df[zip_col].replace(
    "", pd.NA
)


# 10. VALIDATE COORDINATES AND REQUIRED VALUES

invalid_lat = (
    clean_df["geolocation_lat"].notna()
    & ~clean_df["geolocation_lat"].between(-90, 90)
)

invalid_lng = (
    clean_df["geolocation_lng"].notna()
    & ~clean_df["geolocation_lng"].between(-180, 180)
)

missing_coordinates = (
    clean_df["geolocation_lat"].isna()
    | clean_df["geolocation_lng"].isna()
)


print("Invalid ZIP prefixes:", int(invalid_zip.sum()))
print("Invalid latitude values:", int(invalid_lat.sum()))
print("Invalid longitude values:", int(invalid_lng.sum()))
print("Rows with missing coordinates:", int(missing_coordinates.sum()))

print("\nMissing values after cleaning:")
print(clean_df.isna().sum())


# 11. REMOVE EXACT DUPLICATE ROWS ONLY

before_dedup = len(clean_df)

clean_df = clean_df.drop_duplicates().copy()

removed_duplicates = before_dedup - len(clean_df)


print("Rows before exact deduplication:", before_dedup)
print("Exact duplicate rows removed:", removed_duplicates)
print("Rows after exact deduplication:", len(clean_df))
print("Remaining exact duplicates:", clean_df.duplicated().sum())


# 12. FINAL VALIDATION# 

# Recalculate validation masks on the final dataset.
final_invalid_zip = ~clean_df[zip_col].str.fullmatch(
    r"\d{5}", na=False
)

final_invalid_lat = (
    clean_df["geolocation_lat"].notna()
    & ~clean_df["geolocation_lat"].between(-90, 90)
)

final_invalid_lng = (
    clean_df["geolocation_lng"].notna()
    & ~clean_df["geolocation_lng"].between(-180, 180)
)

final_missing_coordinates = (
    clean_df["geolocation_lat"].isna()
    | clean_df["geolocation_lng"].isna()
)


print("Original rows:", len(df))
print("Final cleaned rows:", len(clean_df))
print("Total rows removed:", len(df) - len(clean_df))

print("Invalid ZIP prefixes:", int(final_invalid_zip.sum()))
print("Invalid latitude values:", int(final_invalid_lat.sum()))
print("Invalid longitude values:", int(final_invalid_lng.sum()))
print(
    "Rows with missing coordinates:",
    int(final_missing_coordinates.sum()),
)

print("Remaining exact duplicates:", clean_df.duplicated().sum())


# Stop rather than silently discard unresolved data-quality issues.
if final_invalid_zip.any():
    raise ValueError(
        "Invalid ZIP prefixes remain. Inspect these records before saving."
    )

if final_invalid_lat.any() or final_invalid_lng.any():
    raise ValueError(
        "Invalid coordinates remain. Inspect these records before saving."
    )

if final_missing_coordinates.any():
    raise ValueError(
        "Missing coordinates remain. Investigate before saving."
    )


# 13. SAVE THE CLEANED DATASET

clean_df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8",
)


# 14. VERIFY THE SAVED FILE

saved_df = pd.read_csv(
    OUTPUT_PATH,
    dtype={
        "geolocation_zip_code_prefix": "string",
        "geolocation_city": "string",
        "geolocation_state": "string",
    },
    encoding="utf-8",
)

print("Saved path:", OUTPUT_PATH)
print("Saved shape:", saved_df.shape)
print("Saved exact duplicates:", saved_df.duplicated().sum())

print("\nSaved São Paulo city count:")
print(saved_df["geolocation_city"].eq("sao paulo").sum())

print(
    "\nFile shape verified:",
    saved_df.shape == clean_df.shape,
)

print(
    "File contents verified:",
    saved_df.equals(clean_df),
)

print("\nGeolocation cleaning script completed successfully.")
