
import pandas as pd
df = pd.read_csv('olist_products_dataset.csv')


# # Basic dataset audit
# print("Dataset shape:", df.shape)

# print("\nColumn names:")
# print(df.columns.tolist())

# print("\nData types and non-null values:")
# df.info()

# print("\nMissing values in each column:")
# print(df.isnull().sum())

# print("\nExact duplicate rows:", df.duplicated().sum())

# print("\nDuplicate product IDs:",
#       df['product_id'].duplicated().sum())

# # Showing all columns in the output
# pd.set_option('display.max_columns', None)

# print("\nFirst 5 rows:")
# print(df.head().to_string())





# #  Inspect rows with missing product information

# missing_product_info = df[
#     df['product_category_name'].isna()
# ]

# print("Rows with missing category:",
#       len(missing_product_info))

# print("\nMissing product information - sample 10 rows:")
# print(missing_product_info.head(10).to_string(index=False))

# # Inspect rows with missing weight or dimensions

# missing_dimensions = df[
#     df[['product_weight_g',
#         'product_length_cm',
#         'product_height_cm',
#         'product_width_cm']].isna().any(axis=1)
# ]

# print("\nRows with missing weight/dimensions:")
# print(missing_dimensions.to_string(index=False))

# #  Count zero and negative numeric values

# numeric_cols = [
#     'product_name_lenght',
#     'product_description_lenght',
#     'product_photos_qty',
#     'product_weight_g',
#     'product_length_cm',
#     'product_height_cm',
#     'product_width_cm'
# ]

# print("\nZero values in numeric columns:")
# print((df[numeric_cols] == 0).sum())

# print("\nNegative values in numeric columns:")
# print((df[numeric_cols] < 0).sum())





# Investigating products with zero weight

# zero_weight = df[df['product_weight_g'] == 0]

# print("Number of zero-weight products:", len(zero_weight))

# print("\nZero-weight product records:")
# print(
#     zero_weight[
#         [
#             'product_id',
#             'product_category_name',
#             'product_weight_g',
#             'product_length_cm',
#             'product_height_cm',
#             'product_width_cm'
#         ]
#     ].to_string(index=False)
# )

# # Check if product IDs are blank or contain only spaces
# print("\nBlank product IDs:",
#       df['product_id'].str.strip().eq('').sum())

# # Check if product IDs contain leading/trailing spaces
# print("Product IDs with surrounding spaces:",
#       (df['product_id'] != df['product_id'].str.strip()).sum())


# Validating the product categories using translation file

# translation_df = pd.read_csv('product_category_name_translation.csv')

# # Categories present in products table
# product_categories = set(
#     df['product_category_name'].dropna().unique()
# )

# # Categories present in translation table
# translation_categories = set(
#     translation_df['product_category_name'].dropna().unique()
# )

# # # Categories that are not present in translation table
# unmatched_categories = product_categories - translation_categories

# print("Unique categories in products table:", len(product_categories))
# print("Unique categories in translation table:", len(translation_categories))
# print("Categories missing from translation table:", len(unmatched_categories))
# print("\nUnmatched categories:")
# print(sorted(unmatched_categories))

# # Inspecting unmatched categories

# unmatched_products = df[
#     df['product_category_name'].isin(unmatched_categories)
# ]

# print("Products in unmatched categories:")
# print(
#     unmatched_products[
#         [
#             'product_id',
#             'product_category_name',
#             'product_name_lenght',
#             'product_description_lenght',
#             'product_photos_qty',
#             'product_weight_g'
#         ]
#     ].to_string(index=False)
# )

# print("\nCount by unmatched category:")
# print(unmatched_products['product_category_name'].value_counts())



# Check missing values and percentages

# missing_summary = pd.DataFrame({
#     'missing_count': df.isnull().sum(),
#     'missing_percentage': (df.isnull().sum() / len(df) * 100).round(2)
# })

# print("Missing values summary:")
# print(missing_summary.to_string())

# print("\nRows with missing product category:",
#       df['product_category_name'].isnull().sum())

# print("\nRows with missing weight:",
#       df['product_weight_g'].isnull().sum())

# print("\nRows with missing dimensions:",
#       df[
#           [
#               'product_length_cm',
#               'product_height_cm',
#               'product_width_cm'
#           ]
#       ].isnull().any(axis=1).sum())



# Inspect products with missing physical details

# missing_physical_details = df[
#     df[
#         [
#             'product_weight_g',
#             'product_length_cm',
#             'product_height_cm',
#             'product_width_cm'
#         ]
#     ].isnull().any(axis=1)
# ]

# print("Products with missing physical details:")
# print(
#     missing_physical_details.to_string(index=False)
# )


# # Correct column name spelling

clean_df = df.copy()

clean_df = clean_df.rename(columns={
    'product_name_lenght': 'product_name_length',
    'product_description_lenght': 'product_description_length'
})

print("Updated column names:")
print(clean_df.columns.tolist())

print("\nShape before cleaning:", df.shape)
print("Shape after column rename:", clean_df.shape)




# # Check numeric data types and decimal values

# numeric_columns = [
#     'product_name_length',
#     'product_description_length',
#     'product_photos_qty',
#     'product_weight_g',
#     'product_length_cm',
#     'product_height_cm',
#     'product_width_cm'
# ]

# print("Data types:")
# print(clean_df[numeric_columns].dtypes)

# print("\nSample numeric values:")
# print(clean_df[numeric_columns].head(10).to_string(index=False))

# print("\nNon-integer values in count/length fields:")
# for col in [
#     'product_name_length',
#     'product_description_length',
#     'product_photos_qty'
# ]:
#     values = clean_df[col].dropna()
#     non_integer_count = (values % 1 != 0).sum()
#     print(f"{col}: {non_integer_count}")




# Step 10: Convert count/length columns to nullable integers

integer_columns = [
    'product_name_length',
    'product_description_length',
    'product_photos_qty'
]

for col in integer_columns:
    clean_df[col] = clean_df[col].astype('Int64')

print("Updated data types:")
print(clean_df[integer_columns].dtypes)

print("\nMissing values after conversion:")
print(clean_df[integer_columns].isnull().sum())

print("\nUpdated sample:")
print(clean_df[integer_columns].head(10).to_string(index=False))



# Step 11: Final validation before saving

print("Final shape:", clean_df.shape)

print("\nDuplicate product IDs:",
      clean_df['product_id'].duplicated().sum())

print("\nExact duplicate rows:",
      clean_df.duplicated().sum())

print("\nMissing values:")
print(clean_df.isnull().sum().to_string())

print("\nNegative values in numeric columns:")
numeric_cols = clean_df.select_dtypes(include='number').columns

for col in numeric_cols:
    print(f"{col}: {(clean_df[col] < 0).sum()}")

print("\nProduct IDs missing or blank:",
      (clean_df['product_id'].isnull().sum()
       + clean_df['product_id'].str.strip().eq('').sum()))



# Step 12: Save cleaned products dataset

output_file = 'olist_products_cleaned.csv'

clean_df.to_csv(output_file, index=False)

print(f"\nCleaned file saved successfully: {output_file}")

# Verify the saved file
saved_df = pd.read_csv(output_file)

print("Saved file shape:", saved_df.shape)
print("Saved file columns:", saved_df.columns.tolist())