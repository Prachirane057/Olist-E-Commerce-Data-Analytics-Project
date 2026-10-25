
import pandas as pd

#  Read and audit the original sellers dataset
df = pd.read_csv('olist_sellers_dataset.csv')

print("Dataset shape:", df.shape)

# print("\nColumn names:")
# print(df.columns.tolist())

# print("\nFirst 5 rows:")
# print(df.head().to_string(index=False))

# print("\nData types:")
# print(df.dtypes)

# print("\nMissing values:")
# print(df.isnull().sum())

# print("\nExact duplicate rows:", df.duplicated().sum())

# print("\nDuplicate seller IDs:",
#       df['seller_id'].duplicated().sum())

# print("\nBlank text values:")
# for col in ['seller_id', 'seller_city', 'seller_state']:
#     print(col, ":", df[col].str.strip().eq('').sum())

# print("\nZIP prefix range:")
# print("Minimum:", df['seller_zip_code_prefix'].min())
# print("Maximum:", df['seller_zip_code_prefix'].max())

# print("\nZIP prefixes below 10000:",
#       (df['seller_zip_code_prefix'] < 10000).sum())

# print("\nSeller state values:")
# print(sorted(df['seller_state'].unique()))






#  Investigate ZIP code prefixes
# No permanent changes to df in this step

# zip_check = df['seller_zip_code_prefix'].astype(str).str.zfill(5)

# print("Original ZIP prefix samples:")
# print(df['seller_zip_code_prefix'].head(15).tolist())

# print("\n5-digit ZIP prefix samples:")
# print(zip_check.head(15).tolist())

# print("\nPrefixes that became 5 digits:")
# print((df['seller_zip_code_prefix'].astype(str).str.len() < 5).sum())

# print("\nAny invalid prefix lengths after formatting:")
# print((zip_check.str.len() != 5).sum())





# Apply ZIP prefix formatting to a separate clean copy

clean_df = df.copy()

clean_df['seller_zip_code_prefix'] = (
    clean_df['seller_zip_code_prefix']
    .astype(str)
    .str.zfill(5)
)

print("Original ZIP column type:", df['seller_zip_code_prefix'].dtype)
print("Cleaned ZIP column type:", clean_df['seller_zip_code_prefix'].dtype)

print("\nOriginal ZIP samples:")
print(df['seller_zip_code_prefix'].head(10).tolist())

print("\nCleaned ZIP samples:")
print(clean_df['seller_zip_code_prefix'].head(10).tolist())

print("\nZIP prefix length counts after cleaning:")
print(clean_df['seller_zip_code_prefix'].str.len().value_counts())

print("\nShape after change:", clean_df.shape)






# STEP 3A: Investigate city names and state codes
# Audit only - no changes in this step

print("Unique seller cities:", clean_df['seller_city'].nunique())
print("Unique seller states:", clean_df['seller_state'].nunique())

print("\nState code counts:")
print(clean_df['seller_state'].value_counts().sort_index().to_string())

print("\nCity names with leading/trailing spaces:",
      (clean_df['seller_city'] != clean_df['seller_city'].str.strip()).sum())

print("\nState codes with leading/trailing spaces:",
      (clean_df['seller_state'] != clean_df['seller_state'].str.strip()).sum())

print("\nCity names with uppercase letters:",
      clean_df['seller_city'].str.contains(r'[A-Z]', regex=True).sum())

print("\nState codes not exactly 2 characters:",
      (clean_df['seller_state'].str.len() != 2).sum())

print("\nSample city names:")
print(sorted(clean_df['seller_city'].unique())[:20])






# STEP 3B: Investigate unusual city names
# Audit only - no changes

city = clean_df['seller_city']

# City names containing digits
cities_with_digits = city[city.str.contains(r'\d', na=False)].unique()

print("Unique city names containing digits:", len(cities_with_digits))
print(sorted(cities_with_digits.tolist())[:50])

# City names ending with a space and two letters
cities_with_suffix = city[
    city.str.contains(r'\s[a-z]{2}$', regex=True, na=False)
].unique()

print("\nUnique city names ending with a 2-letter suffix:",
      len(cities_with_suffix))
print(sorted(cities_with_suffix.tolist())[:50])

# Show seller records for city names containing digits
print("\nRecords with digits in city name:")
print(
    clean_df[city.str.contains(r'\d', na=False)]
    [['seller_id', 'seller_city', 'seller_state']]
    .to_string(index=False)
)



print(
    clean_df[clean_df['seller_city'] == '04482255']
    [['seller_id', 'seller_zip_code_prefix', 'seller_city', 'seller_state']]
    .to_string(index=False)
)




# STEP 3C: Inspect city names with possible state suffixes

suffix_cities = [
    'aguas claras df',
    'angra dos reis rj',
    'brasilia df',
    'cariacica / es',
    'lages - sc',
    'mogi das cruzes / sp',
    'sao paulo - sp',
    'sao paulo sp',
    'sp / sp'
]

print("\nRecords with possible state suffixes:")

print(
    clean_df[clean_df['seller_city'].isin(suffix_cities)]
    [['seller_zip_code_prefix', 'seller_city', 'seller_state']]
    .sort_values(['seller_state', 'seller_city'])
    .to_string(index=False)
)




# STEP 4: Final validation before saving

print("Final dataset shape:", clean_df.shape)

print("\nMissing values:")
print(clean_df.isnull().sum())

print("\nExact duplicate rows:", clean_df.duplicated().sum())

print("\nDuplicate seller IDs:",
      clean_df['seller_id'].duplicated().sum())

print("\nZIP prefix lengths:")
print(clean_df['seller_zip_code_prefix'].str.len().value_counts())

print("\nBlank text values:")
for col in ['seller_id', 'seller_city', 'seller_state']:
    print(col, ":", clean_df[col].str.strip().eq('').sum())

print("\nData types:")
print(clean_df.dtypes)






# STEP 5: Save the cleaned dataset separately

output_file = 'olist_sellers_cleaned.csv'

clean_df.to_csv(output_file, index=False)

print("\nCleaned dataset saved successfully:", output_file)

# Verify the saved file
saved_df = pd.read_csv(
    output_file,
    dtype={'seller_zip_code_prefix': str}
)

print("Saved dataset shape:", saved_df.shape)
print("Saved columns:", saved_df.columns.tolist())
print(
    "All ZIP prefixes have 5 characters:",
    saved_df['seller_zip_code_prefix'].str.len().eq(5).all()
)
