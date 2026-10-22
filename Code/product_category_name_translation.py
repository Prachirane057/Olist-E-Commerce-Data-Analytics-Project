
import pandas as pd

# STEP 1: Read and audit translation dataset
df = pd.read_csv('product_category_name_translation.csv')

print("Dataset shape:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 10 rows:")
print(df.head(10).to_string(index=False))

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nExact duplicate rows:", df.duplicated().sum())

print("\nDuplicate Portuguese categories:",
      df['product_category_name'].duplicated().sum())

print("\nDuplicate English translations:",
      df['product_category_name_english'].duplicated().sum())

print("\nBlank values:")
for col in df.columns:
    print(col, ":", df[col].astype('string').str.strip().eq('').sum())

print("\nLeading/trailing spaces:")
for col in df.columns:
    print(col, ":",
          (df[col] != df[col].astype('string').str.strip()).sum())






# STEP 2: Check translation coverage against products dataset

products_df = pd.read_csv('olist_products_dataset.csv')

translation_categories = set(
    df['product_category_name'].dropna()
)

product_categories = set(
    products_df['product_category_name'].dropna()
)

# Categories used in products but missing from translation table
untranslated = product_categories - translation_categories

# Translation categories not used in products
unused_translations = translation_categories - product_categories

print("Unique categories in products:",
      len(product_categories))

print("Unique categories in translation file:",
      len(translation_categories))

print("\nProduct categories without translations:",
      len(untranslated))
print(sorted(untranslated))

print("\nTranslation categories not used in products:",
      len(unused_translations))
print(sorted(unused_translations))

print("\nProducts with missing category:",
      products_df['product_category_name'].isna().sum())
