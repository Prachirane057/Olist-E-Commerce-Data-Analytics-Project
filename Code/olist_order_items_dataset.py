import pandas as pd
df = pd.read_csv('olist_order_items_dataset.csv')
# print(df)

#dataset information 
# print(df.info())

# #identify the missing values form each coloumn
# missing_values= df.isnull().sum()
# print(missing_values)


#identify datatypes of each coloum
# data_type= df.dtypes
# print(data_type)
 
# number of rows and coloumns in the dataset
# shape= df.shape
# print(shape)

# coloum names
# print(df.columns.tolist())

# Duplicates 
# duplicates= df.duplicated().sum()
# print(duplicates)

# printing first 5 rows
# print(df.head(5))


# VALIDATING THE DATASET

# finding unique orders 
# unique_order_id= df['order_id'].nunique()
# print(unique_order_id)

# unique order_item id
# unique_order_item = sorted(df['order_item_id'].unique())
# print(unique_order_item)

# order item frequency 
# print(df['order_item_id'].value_counts().sort_index())

#duplicate order_id +order_item_id combinations 
# print(df.duplicated(subset=['order_id','order_item_id']).sum())

# order item id's who are less than 0 or 1
# print((df['order_item_id']<= 0).sum())


#validating shipping dates 
# dates = pd.to_datetime(
#     df['shipping_limit_date'],
#     errors='coerce'
# )

# print("Invalid shipping dates:", dates.isna().sum())
# print("Earliest shipping date:", dates.min())
# print("Latest shipping date:", dates.max())

# Validate numeric values
# print("\nPrice <= 0:", (df['price'] <= 0).sum())
# print("Freight value < 0:", (df['freight_value'] < 0).sum())

# print("\nPrice summary:")
# print(df['price'].describe())

# print("\nFreight value summary:")
# print(df['freight_value'].describe())



# Check item numbering within each order

# item_counts = df.groupby('order_id')['order_item_id'].agg(
#     ['count', 'min', 'max', 'nunique']
# )

# print("Orders with item numbering not starting at 1:",
#       (item_counts['min'] != 1).sum())

# print("Orders with possible numbering gaps:",
#       (item_counts['max'] != item_counts['count']).sum())

# #Check shipping date strings

# print("\nSample shipping dates:")
# print(df['shipping_limit_date'].head(10).to_string(index=False))

# # Review unusually high prices

# print("\nTop 10 highest-priced items:")
# print(
#     df.nlargest(10, 'price')[
#         ['order_id', 'order_item_id', 'product_id',
#          'price', 'freight_value', 'shipping_limit_date']
#     ].to_string(index=False)
# )



# # Step 5: Validate product and seller IDs

# products = pd.read_csv('olist_products_dataset.csv')
# sellers = pd.read_csv('olist_sellers_dataset.csv')

# # Check product IDs
# product_ids = set(products['product_id'])
# missing_products = ~df['product_id'].isin(product_ids)

# print("Order items with product IDs not found in products table:",
#       missing_products.sum())

# # Check seller IDs
# seller_ids = set(sellers['seller_id'])
# missing_sellers = ~df['seller_id'].isin(seller_ids)

# print("Order items with seller IDs not found in sellers table:",
#       missing_sellers.sum())



# Step 6: Create a cleaned copy in memory
# clean_df = df.copy()

# # Convert shipping_limit_date to datetime
# clean_df['shipping_limit_date'] = pd.to_datetime(
#     clean_df['shipping_limit_date'],
#     errors='raise'
# )

# # Verify data types
# print(clean_df.dtypes)

# # Verify shape is unchanged
# print("\nOriginal shape:", df.shape)
# print("Cleaned shape:", clean_df.shape)

# # Verify missing values after conversion
# print("\nMissing values after conversion:")
# print(clean_df.isna().sum())




# Create the cleaned copy
# clean_df = df.copy()

# # Convert the date column
# clean_df['shipping_limit_date'] = pd.to_datetime(
#     clean_df['shipping_limit_date'],
#     errors='raise'
# )

# # Save the cleaned dataset
# output_file = 'olist_order_items_cleaned.csv'
# clean_df.to_csv(output_file, index=False)

# print(f"Cleaned file saved as: {output_file}")

