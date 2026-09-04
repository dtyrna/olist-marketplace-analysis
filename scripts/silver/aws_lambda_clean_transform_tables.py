import pandas as pd
import numpy as np
#pip install unidecode
from unidecode import unidecode
from pathlib import Path


##############################################################################
# Begin Code Patrick
##############################################################################

print("====================================================================")
print("Load from Pickle".upper())
print("====================================================================\n")

#setting working directory


SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = SCRIPTS_DIR.parent


last_layer = "bronze"
current_layer = "silver"
source_path = SCRIPTS_DIR / last_layer  # .../scripts/bronze
source_type = ".pkl"

bronze_tables_path = source_path / f"{last_layer}_tables{source_type}"

bronze_tables_dict = pd.read_pickle(bronze_tables_path)


print(f"Pickle Tables ({", ".join(bronze_tables_dict.keys())}) successsfully loaded into {current_layer}-Layer!\n")

print("order_payments:\n")
print(bronze_tables_dict["bronze.csv_order_payments.csv"].head(3))
print("\n")

print("products:\n")
print(bronze_tables_dict["bronze.csv_products.csv"].head(3))
print("\n")

print("sellers:\n")
print(bronze_tables_dict["bronze.csv_sellers.csv"].head(3))
print("\n")



df_order_payments = bronze_tables_dict["bronze.csv_order_payments.csv"]
df_products = bronze_tables_dict["bronze.csv_products.csv"]
df_sellers = bronze_tables_dict["bronze.csv_sellers.csv"]

print("\n")


print("====================================================================")
print("Start Cleaning order_payments".upper())
print("====================================================================\n")

print(df_order_payments.head(3))

print("\n")

# ### Explain the columns

# **order_id**: 
# unique identifier of an order

# **payment_sequential**: 
# a customer may pay an order with more than one payment method. If he does so, a sequence will be created to accommodate all payments

# **payment_type**: 
# method of payment chosen by the customer

# **payment_installments**: 
# number of installments chosen by the customer

# **payment_value**: 
# transaction value

print("====================================================================")
print("Convert columns".upper())
print("====================================================================\n")

numeric_columns = ["payment_sequential", "payment_installments", "payment_value"]
string_columns = ["order_id", "payment_type"]


for col in numeric_columns:

    try:
        df_order_payments[col] = pd.to_numeric(df_order_payments[col], errors="raise")
        print(f"{col} successfully converted into {df_order_payments[col].dtype}")
        
    except Execution as e:
        print(f"Error in converting {col} into numeric")
        print(f"Error details: {e}")
        sys.exit(1)

for col in string_columns:

    try:
        df_order_payments[col] = df_order_payments[col].astype("str")
        print(f"{col} successfully converted into {df_order_payments[col].dtype}")
        
    except Execution as e:
        print(f"Error in converting {col} into string")
        print(f"Error details: {e}")
        sys.exit(1)

print("\n")

print("====================================================================")
print("Check Data Quality".upper())
print("====================================================================\n")

print(df_order_payments.info())

print("\n")

print("====================================================================")
print("payment_type")
print("====================================================================\n")

print(f"""
payment_type has the following values: 
{df_order_payments["payment_type"].value_counts()}
\n""")

#dropping rows with 'not_defined' payment_type

payment_type_is_not_defined_count = df_order_payments[df_order_payments.payment_type == "not_defined"].shape[0]
df_order_payments = df_order_payments[df_order_payments.payment_type != "not_defined"]
print(f"{payment_type_is_not_defined_count} rows with payment_type 'not_defined' were dropped\n")

print("====================================================================")
print("payment_installments")
print("====================================================================\n")

print(f"""
payment_installments has the following statistic values:
{df_order_payments["payment_installments"].describe()}
\n""")

print("====================================================================")
print("payment_sequential")
print("====================================================================\n")

print(f"""
payment_sequential has the following statistic values:
{df_order_payments["payment_sequential"].describe()}
\n""")

print("====================================================================")
print("payment_value")
print("====================================================================\n")


print(f"""
payment_value has the following statistic values:
{df_order_payments["payment_value"].describe()}
\n""")

#dropping rows with '0.0' payment_value

payment_value_is_zero_count = df_order_payments[df_order_payments.payment_value == 0].shape[0]
df_order_payments = df_order_payments[df_order_payments.payment_value != 0]
print(f"{payment_value_is_zero_count} rows with payment_value '0.0' were dropped\n")

print("====================================================================")
print("Built a unique key")
print("====================================================================\n")

#starts at 1

df_order_payments["id_order_payments"] = np.arange(1, df_order_payments.shape[0] + 1)
sorted_columns = df_order_payments.columns.sort_values()
df_order_payments = df_order_payments[sorted_columns]
#df_order_payments


print("====================================================================")
print("Start Cleaning products".upper())
print("====================================================================\n")

print(df_products.head(3))

print("\n")

# ### Explain the columns

# **product_id**: 
# unique product identifier

# **product_category_name**: 
# root category of product, in Portuguese

# **product_name_lenght**: 
# number of characters extracted from the product name


# **product_description_lenght**: 
# number of characters extracted from the product description


# **product_photos_qty**: 
# number of product published photos


# **product_weight_g**:
# product weight measured in grams


# **product_length_cm**:
# product length measured in centimeters


# **product_height_cm**:
# product height measured in centimeters


# **product_width_cm**:
# product width measured in centimeters

print("====================================================================")
print("Convert columns".upper())
print("====================================================================\n")

numeric_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
    ]

string_columns = [
    "product_id",
    "product_category_name"
]


for col in numeric_columns:

    try:
        df_products[col] = pd.to_numeric(df_products[col], errors="raise")
        print(f"{col} successfully converted into {df_products[col].dtype}")
        
    except Execution as e:
        print(f"Error in converting {col} into numeric")
        print(f"Error details: {e}")
        sys.exit(1) #exit script to avoid errors

for col in string_columns:

    try:
        df_products[col] = df_products[col].astype("str")
        print(f"{col} successfully converted into {df_products[col].dtype}")
        
    except Execution as e:
        print(f"Error in converting {col} into string")
        print(f"Error details: {e}")
        sys.exit(1)

print("\n")

print("====================================================================")
print("Check Data Quality".upper())
print("====================================================================\n")

print(df_products.info())

print("\n")


print("====================================================================")
print("product_id")
print("====================================================================\n")

#check uniqueness of product_id

if (df_products.dropna(subset= "product_id").shape[0] == df_products.shape[0]) & (df_products.product_id.nunique() == df_products.product_id.shape[0]):
    print("Every row has a product_id and they are unique")
    product_id_uniqueness = True

elif df_products.dropna(subset= "product_id").shape[0] < df_products.shape[0]:
    
    print(f"""
    There are {df_products.shape[0] - df_products.dropna(subset= "product_id").shape[0]} rows without a product_id
    """)

else:
    print(f"""
    There are duplicates in product_id:
    {print(df_products[df_products.duplicated(subset="product_id", keep=False)].sort_values(by="product_id"))}
    """)
    sys.exit(1) #exit script to avoid errors

print("\n")

#Are there rows, where all data columns (without product_id) are null?

empty_data_rows_count = df_products[df_products.drop("product_id", axis=1).isnull().all(axis=1)].shape[0]
empty_data_rows_with_product_id_count = df_products[df_products.drop("product_id", axis=1).isnull().all(axis=1)].dropna(subset= "product_id").shape[0]
empty_rows_without_product_id_count = empty_data_rows_count - empty_data_rows_with_product_id_count

data_columns = df_products.columns.drop("product_id")

if empty_data_rows_count > 0:
    
    print(f"{empty_data_rows_count} products don't have data in data columns")
    print(f"{empty_data_rows_with_product_id_count} products have only a product_id and don't have data")
    print(f"{empty_rows_without_product_id_count} products don't have any data\n")

    #drop rows without data in data columns

    df_products = df_products.dropna(subset=data_columns, how="all")
    empty_data_rows_after_drop_count = df_products[df_products.drop("product_id", axis=1).isnull().all(axis=1)].shape[0]

    if empty_data_rows_count - empty_data_rows_after_drop_count == empty_data_rows_count:
        print(f"Every product without data in data columns ({", ".join(data_columns)}) were dropped.\n")
    else:
        print("There was a problem by dropping empty data rows\n")

else:
    print("There are no products without data\n")



print("====================================================================")
print("product_category_name")
print("====================================================================\n")

#check, if products have multiple categories

category_seperator_list = [",", ";", " "]

for sep in category_seperator_list:

    if df_products[(df_products.product_category_name != df_products.product_category_name.str.replace(sep,"")) & (df_products.product_category_name.isnull() == False)].shape[0] == 0:
        print(f"There are no products, which have multiple categories seperated with '{sep}'")

    else:
        print(f"There are products, which have multiple categories seperated with '{sep}':\n")
        print(df_products[(df_products.product_category_name != df_products.product_category_name.str.replace(sep,"")) & (df_products.product_category_name.isnull() == False)][["product_id", "product_category_name"]])

print("\n")

print(f"product_category_name has {df_products.product_category_name.nunique()} unique categories")
print(f"In product_category_name {df_products.product_category_name.isnull().sum()} of {df_products.shape[0]} products don't have any category (NULL values)\n")

print("====================================================================")
print("product_description_lenght")
print("====================================================================\n")

print(f"product_description_lenght is from {df_products.product_description_lenght.min():.0f} up to {df_products.product_description_lenght.max():.0f} characters and the mean description lenght is {df_products.product_description_lenght.mean():.0f}")
print(f"In product_description_lenght {df_products.product_description_lenght.isnull().sum()} of {df_products.shape[0]} products don't have a description (NULL values)\n")

print("====================================================================")
print("product_photos_qty")
print("====================================================================\n")

print(f"product_photos_qty is from {df_products.product_photos_qty.min():.0f} up to {df_products.product_photos_qty.max():.0f} photos per product and the mean photo quantity is {df_products.product_photos_qty.mean():.0f}")
print(f"In product_photos_qty {df_products.product_photos_qty.isnull().sum()} of {df_products.shape[0]} products don't have any photo (NULL values)\n")



#Are there products without a category, description and photos?

data_columns = ["product_category_name", "product_description_lenght", "product_photos_qty"]

empty_data_rows_count = df_products[df_products[data_columns].isnull().all(axis=1)].shape[0]



if empty_data_rows_count > 0:
    
    print(f"{empty_data_rows_count} of {df_products.shape[0]} rows don't have data in any data column ({", ".join(data_columns)}):\n")
    print(df_products[df_products[data_columns].isnull().all(axis=1)].head(3))

else:
    print(f"There are no products without data in {", ".join(data_columns)}")

print("\n")


print("====================================================================")
print("product_weight_g, product_length_cm, product_height_cm, product_width_cm")
print("====================================================================\n")

#product_weight_g

print(f"product_weight_g is from {df_products.product_weight_g.min():.0f} up to {df_products.product_weight_g.max():.0f} grams per product and the mean weight is {df_products.product_weight_g.mean():.0f}")
print(f"In product_weight_g {df_products.product_weight_g.isnull().sum()} of {df_products.shape[0]} products don't have any weight\n")

#product_length_cm

print(f"product_length_cm is from {df_products.product_length_cm.min():.0f} up to {df_products.product_length_cm.max():.0f} centimetres per product and the mean lenghth is {df_products.product_length_cm.mean():.0f}")
print(f"In product_length_cm {df_products.product_length_cm.isnull().sum()} of {df_products.shape[0]} products don't have any length\n")

#product_height_cm

print(f"product_height_cm is from {df_products.product_height_cm.min():.0f} up to {df_products.product_height_cm.max():.0f} centimetres per product and the mean height is {df_products.product_height_cm.mean():.0f}")
print(f"In product_height_cm {df_products.product_height_cm.isnull().sum()} of {df_products.shape[0]} products don't have any height\n")

#product_width_cm

print(f"product_width_cm is from {df_products.product_width_cm.min():.0f} up to {df_products.product_width_cm.max():.0f} centimetres per product and the mean width is {df_products.product_width_cm.mean():.0f}")
print(f"In product_width_cm {df_products.product_width_cm.isnull().sum()} of {df_products.shape[0]} products don't have any width\n")


#Are there products without data in size columns?

data_columns = ["product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]
empty_data_rows_count = df_products[df_products[data_columns].isnull().all(axis=1)].shape[0]

if empty_data_rows_count > 0:
    
    print(f"{empty_data_rows_count} of {df_products.shape[0]} rows don't have data in any data column ({", ".join(data_columns)}):\n")
    print(df_products[df_products[data_columns].isnull().all(axis=1)].head())

else:
    print(f"There no products without data in all size columns ({", ".join(data_columns)})")
    
print("\n")

print("====================================================================")
print("Built a shorter unique key")
print("====================================================================\n")

if product_id_uniqueness == True:
    
    #starts at 1
    df_products["id_products"] = np.arange(1, df_products.shape[0] + 1)

sorted_columns = df_products.columns.sort_values()
df_products = df_products[sorted_columns]
#df_products

print("====================================================================")
print("Start Cleaning sellers".upper())
print("====================================================================\n")

print(df_sellers.head(3))

print("\n")

# ### Explain the columns

# **seller_id**: 
# seller unique identifier

# **seller_zip_code_prefix**: 
# first 5 digits of seller zip code

# **seller_city**: 
# seller city name

# **seller_state**: 
# seller state

print("====================================================================")
print("Convert columns".upper())
print("====================================================================\n")

string_columns = [
    "seller_id",
    "seller_zip_code_prefix",
    "seller_city",
    "seller_state"
]

for col in string_columns:

    try:
        df_sellers[col] = df_sellers[col].astype("str")
        print(f"{col} successfully converted into {df_sellers[col].dtype}")
        
    except Execution as e:
        print(f"Error in converting {col} into string")
        print(f"Error details: {e}")
        sys.exit(1)

print("\n")

print("====================================================================")
print("Check Data Quality".upper())
print("====================================================================\n")

print(df_sellers.info())

print("\n")

#check uniqueness of seller_id

if (df_sellers.dropna(subset= "seller_id").shape[0] == df_sellers.shape[0]) & (df_sellers.seller_id.nunique() == df_sellers.seller_id.shape[0]):
    print("Every row has a seller_id and they are unique")
    seller_id_uniqueness = True

elif df_sellers.dropna(subset= "seller_id").shape[0] < df_sellers.shape[0]:
    
    print(f"""
    There are {df_sellers.shape[0] - df_sellers.dropna(subset= "seller_id").shape[0]} rows without a seller_id
    """)

else:
    print(f"""
    There are duplicates in seller_id:
    {print(df_sellers[df_sellers.duplicated(subset="seller_id", keep=False)].sort_values(by="seller_id"))}
    """)
    sys.exit(1) #exit script to avoid errors

print("\n")

#Are there rows, where all data columns (without seller_id) are null?

empty_data_rows_count = df_sellers[df_sellers.drop("seller_id", axis=1).isnull().all(axis=1)].shape[0]
empty_data_rows_with_seller_id_count = df_sellers[df_sellers.drop("seller_id", axis=1).isnull().all(axis=1)].dropna(subset= "seller_id").shape[0]
empty_rows_without_seller_id_count = empty_data_rows_count - empty_data_rows_with_seller_id_count

data_columns = df_sellers.columns.drop("seller_id")

if empty_data_rows_count > 0:
    
    print(f"{empty_data_rows_count} rows don't have data in data columns")
    print(f"{empty_data_rows_with_seller_id_count} rows have only a seller_id and don't have data")
    print(f"{empty_rows_without_seller_id_count} rows don't have any data\n")

    #drop rows without data in data columns

    df_sellers = df_sellers.dropna(subset=data_columns, how="all")
    empty_data_rows_after_drop_count = df_sellers[df_sellers.drop("seller_id", axis=1).isnull().all(axis=1)].shape[0]

    if empty_data_rows_count - empty_data_rows_after_drop_count == empty_data_rows_count:
        print(f"Every row without data in data columns ({", ".join(data_columns)}) were dropped.\n")
    else:
        print("There was a problem by dropping empty data rows\n")

else:
    print(f"There are no seller_id without data in data columns ({", ".join(data_columns)})\n")


print("====================================================================")
print("seller_zip_code_prefix")
print("====================================================================\n")

print(df_sellers.seller_zip_code_prefix.value_counts().describe())

print("\n")

print(f"""
There are zip code prefix regions where only {df_sellers.seller_zip_code_prefix.value_counts().min():.0f} sellers are located
and regions there are {df_sellers.seller_zip_code_prefix.value_counts().max():.0f} sellers located.
In average there are {df_sellers.seller_zip_code_prefix.value_counts().mean():.0f} seller per zip code prefix region
\n""")

print("====================================================================")
print("seller_city")
print("====================================================================\n")

#Check special characters in letters in "seller_city"

cities_with_special_chars = df_sellers[df_sellers["seller_city"].str.lower().apply(unidecode) != df_sellers["seller_city"]]

if cities_with_special_chars.shape[0] > 0:

    print(f"""
    {", ".join(cities_with_special_chars.seller_city)} are cities with special characters as letters.
    Convert to english character set... 
    \n""")
    df_sellers["seller_city"] = df_sellers["seller_city"].apply(unidecode)
    cities_with_special_chars = df_sellers[df_sellers["seller_city"].str.lower().apply(unidecode) != df_sellers["seller_city"]]

    if cities_with_special_chars.shape[0] == 0:
        print(f"Cities were successfully converted into english character set\n")
    else:
        print(f"There was a problem by convert {cities_with_special_chars.shape[0]} cities.\n")

else:
    print("There are no cities with special characters as letters\n")



#check, if there are cities with special characters

special_characters_list = [",", ";", "/"]


for char in special_characters_list:

    cities_with_special_chars = df_sellers[(df_sellers.seller_city != df_sellers.seller_city.str.replace(char,"")) & (df_sellers.seller_city.isnull() == False)]

    if cities_with_special_chars.shape[0] == 0:
        print(f"There are no cities, which special characters '{char}'\n")

    else:
        print(f"There are {cities_with_special_chars.shape[0]} cities, with special character '{char}':\n")
        print(f"{"\n".join(cities_with_special_chars["seller_city"])}")
        print(f"\n... keep only city before '{char}' ...\n")
        
        df_sellers["seller_city"]= df_sellers["seller_city"].str.split(char).str[0].str.strip()

        if df_sellers[df_sellers["seller_city"] != df_sellers["seller_city"].str.replace(char, "")].shape[0] == 0:
            print(f"Cities with '{char}' succesfully cleaned\n")
        
        else:
            print(f"There was a problem by splitting on '{char}'\n")

df_sellers["seller_city"] = df_sellers["seller_city"].astype("str")

print("====================================================================")
print("seller_state")
print("====================================================================\n")

#check, if there special characters or different writings

seller_state_list = []
uncorrect_counter = 0

for unique in df_sellers["seller_state"].unique():
    
    seller_state_list.append(unique)

seller_state_list.sort()
print(f"The unique seller_states are: {", ".join(seller_state_list)}\n")


for state in seller_state_list:

    if state != state.lower().strip() or len(state) != 2:

        print(f"The state '{state}' is not in the correct format (2 capital letters)")
        uncorrect_counter += 1
        print("\n... correct the format in seller_state ...\n")
        corrected_state = state.lower().strip()[:2]
        # replace_list.append(state)
        # replace_into_list.append(state.upper().strip()[:2])
        
        df_sellers.seller_state = df_sellers.seller_state.str.replace(state, corrected_state)

        if df_sellers[df_sellers.seller_state == state].shape[0] == 0:
            print(f"Successfully correct the format of '{state}' into '{corrected_state}'\n")

        else:
            print(f"There was a problem by correct '{state}' into '{corrected_state}'\n")
    
if uncorrect_counter == 0:    
    
    print(f"All states are correct formatted\n")


print("====================================================================")
print("Built a shorter unique key")
print("====================================================================\n")

if seller_id_uniqueness == True:
    
    #starts at 1
    df_sellers["id_sellers"] = np.arange(1, df_sellers.shape[0] + 1)
    
sorted_columns = df_sellers.columns.sort_values()
df_sellers = df_sellers[sorted_columns]
#df_sellers

##############################################################################
# End Code Patrick
##############################################################################


##############################################################################
# Start Code David
##############################################################################

# ============================================================
# OLIST MARKETPLACE – SILVER CLEANING
# CUSTOMERS, ORDERS & ORDER REVIEWS
# ============================================================
#
# This script combines the three existing preprocessing
# pipelines into one reproducible Silver-layer workflow.
#
# The script expects the Bronze DataFrames
# `bronze_customers`, `bronze_orders`, and
# `bronze_order_reviews` to already be available.
#
# Output DataFrames:
# - silver_customers
# - silver_orders
# - silver_order_reviews
#
# No records are intentionally removed by the preprocessing
# logic. Original source identifiers and relevant source
# values are preserved.
#
# ============================================================


# ============================================================
# 1. COMMON IMPORT & LOCAL BRONZE DATA LOAD
# ============================================================
#
# This block is intentionally inactive.
# The common project script is responsible for imports
# and loading the Bronze datasets.
#
# ------------------------------------------------------------
# Local project version
# ------------------------------------------------------------

# import pandas as pd
# import numpy as np
# from pathlib import Path

# pd.set_option("display.max_columns", None)
# pd.set_option("display.max_rows", 100)


# def find_project_root():
#     """
#     Find the project root by looking for the expected
#     datasets/raw and datasets/processed directories.
#     """
#     current_path = Path.cwd()

#     for path in [current_path, *current_path.parents]:
#         if (
#             (path / "datasets" / "raw").exists()
#             and (path / "datasets" / "processed").exists()
#         ):
#             return path

#     raise FileNotFoundError(
#         "Project root could not be found. "
#         "Expected 'datasets/raw' and 'datasets/processed' directories."
#     )


# PROJECT_ROOT = find_project_root()

# RAW_PATH = PROJECT_ROOT / "datasets" / "raw"
# PROCESSED_PATH = PROJECT_ROOT / "datasets" / "processed"

# PROCESSED_PATH.mkdir(parents=True, exist_ok=True)


# bronze_customers = pd.read_csv(
#     RAW_PATH / "olist_customers_dataset.csv"
# )

# bronze_orders = pd.read_csv(
#     RAW_PATH / "olist_orders_dataset.csv"
# )

# bronze_order_reviews = pd.read_csv(
#     RAW_PATH / "olist_order_reviews_dataset_en.csv"
#)


# customers_raw_row_count = len(bronze_customers)
# orders_raw_row_count = len(bronze_orders)
# order_reviews_raw_row_count = len(bronze_order_reviews)


# ============================================================
# 1B. AWS S3 BRONZE DATA LOAD – LAMBDA VERSION
# ============================================================
#
# This block is intentionally inactive.
# It is used when AWS Lambda loads the Bronze datasets
# directly from S3.
#
# ------------------------------------------------------------
# S3 data flow
#
# S3 raw/
#     |
#     v
# AWS Lambda
#     |
#     v
# Silver processing
#     |
#     v
# S3 processed/
# ------------------------------------------------------------

# import boto3
# from io import StringIO

# S3_BUCKET = "dsi-final-project-360964564955-eu-central-1-an"

# RAW_PREFIX = "raw/"
# PROCESSED_PREFIX = "processed/"

# s3 = boto3.client("s3")


# def load_csv_from_s3(bucket, key):
#     """
#     Load a CSV file from S3 into a pandas DataFrame.
#     """
#     response = s3.get_object(
#         Bucket=bucket,
#         Key=key
#     )

#     return pd.read_csv(response["Body"])


# bronze_customers = load_csv_from_s3(
#     S3_BUCKET,
#     f"{RAW_PREFIX}olist_customers_dataset.csv"
# )

# bronze_orders = load_csv_from_s3(
#     S3_BUCKET,
#     f"{RAW_PREFIX}olist_orders_dataset.csv"
# )

# bronze_order_reviews = load_csv_from_s3(
#     S3_BUCKET,
#     f"{RAW_PREFIX}olist_order_reviews_dataset_en.csv"
# )


# customers_raw_row_count = len(bronze_customers)
# orders_raw_row_count = len(bronze_orders)
# order_reviews_raw_row_count = len(bronze_order_reviews)


# ============================================================
# 2. CUSTOMERS – SILVER PREPROCESSING
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMERS – SILVER PREPROCESSING")
print("=" * 60)


# ------------------------------------------------------------
# 2.1 Data Audit
# ------------------------------------------------------------

print("Shape:", bronze_customers.shape)
print("\nColumns:")
print(bronze_customers.columns.tolist())

print("\nData types:")
print(bronze_customers.dtypes)

print("\nMissing values:")
print(bronze_customers.isna().sum())

print("\nDuplicate rows:", bronze_customers.duplicated().sum())

print("\nUnique customer_id:", bronze_customers["customer_id"].nunique())
print(
    "Unique customer_unique_id:",
    bronze_customers["customer_unique_id"].nunique()
)
print(
    "customer_id is unique:",
    bronze_customers["customer_id"].is_unique
)


# ------------------------------------------------------------
# 2.2 Customer Record Analysis
# ------------------------------------------------------------

customer_counts = (
    bronze_customers
    .groupby("customer_unique_id")
    .size()
    .sort_values(ascending=False)
)

print(
    "Customers with multiple customer records:",
    (customer_counts > 1).sum()
)

repeat_customer_records = customer_counts[
    customer_counts > 1
]

print("\nDistribution of customer record counts:")
print(customer_counts.value_counts().sort_index())

print("\nRepeated customer records summary:")
print(repeat_customer_records.describe())

print(
    "\nTotal records belonging to repeated customers:",
    repeat_customer_records.sum()
)


# ------------------------------------------------------------
# 2.3 Customer Location Analysis
# ------------------------------------------------------------

print("Customer state distribution:")
print(bronze_customers["customer_state"].value_counts())

print(
    "Unique cities:",
    bronze_customers["customer_city"].nunique()
)

print("\nZIP code summary:")
print(bronze_customers["customer_zip_code_prefix"].describe())

print(
    "Unique ZIP code prefixes:",
    bronze_customers["customer_zip_code_prefix"].nunique()
)

print(
    "Negative ZIP code prefixes:",
    (
        bronze_customers["customer_zip_code_prefix"] < 0
    ).sum()
)

print(
    "Missing ZIP code prefixes:",
    bronze_customers["customer_zip_code_prefix"].isna().sum()
)


# ------------------------------------------------------------
# 2.4 Cleaning & Standardization
# ------------------------------------------------------------

# Create the Silver working copy
silver_customers = bronze_customers.copy()

# Create technical Silver key
silver_customers.insert(
    0,
    "id_customers",
    range(1, len(silver_customers) + 1)
)

# Trim whitespace from string fields
string_columns = [
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state"
]

for column in string_columns:
    silver_customers[column] = (
        silver_customers[column].str.strip()
    )

# Standardize state values
silver_customers["customer_state"] = (
    silver_customers["customer_state"]
    .str.lower()
)

# Standardize city values
silver_customers["customer_city"] = (
    silver_customers["customer_city"]
    .str.lower()
    .str.replace("-", " ", regex=False)
    .str.replace("'", "", regex=False)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# Replace the identified incorrect city value
silver_customers.loc[
    silver_customers["customer_city"] == "quilometro 14 do mutum",
    "customer_city"
] = "mutum"

# Define explicit data types
silver_customers["customer_id"] = (
    silver_customers["customer_id"].astype("string")
)

silver_customers["customer_unique_id"] = (
    silver_customers["customer_unique_id"].astype("string")
)

silver_customers["customer_city"] = (
    silver_customers["customer_city"].astype("string")
)

silver_customers["customer_state"] = (
    silver_customers["customer_state"].astype("string")
)

silver_customers["customer_zip_code_prefix"] = (
    silver_customers["customer_zip_code_prefix"]
    .astype("string")
    .str.zfill(5)
)


# ------------------------------------------------------------
# 2.5 Customers – Data Quality Validation
# ------------------------------------------------------------

valid_states = {
    "sp", "sc", "mg", "pr", "rj", "rs", "pa", "go", "es", "ba",
    "ma", "ms", "ce", "df", "rn", "pe", "mt", "am", "ap", "al",
    "ro", "pb", "to", "pi", "ac", "se", "rr"
}

invalid_states = (
    set(silver_customers["customer_state"].dropna().unique())
    - valid_states
)

assert silver_customers["customer_id"].notna().all()
assert silver_customers["customer_id"].is_unique

assert silver_customers["customer_unique_id"].notna().all()

assert (
    silver_customers["customer_zip_code_prefix"]
    .str.len()
    .eq(5)
    .all()
)

assert (
    silver_customers["customer_zip_code_prefix"]
    .str.isnumeric()
    .all()
)

expected_customers_columns = [
    "id_customers",
    "customer_id",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state"
]

assert (
    silver_customers.columns.tolist()
    == expected_customers_columns
)

assert len(silver_customers) == customers_raw_row_count

assert silver_customers["id_customers"].notna().all()
assert silver_customers["id_customers"].is_unique
assert silver_customers["id_customers"].min() == 1
assert silver_customers["id_customers"].max() == len(
    silver_customers
)

assert (
    silver_customers["customer_city"]
    .str.match(r"^[a-z\s]+$")
    .all()
)

assert (
    silver_customers["customer_city"]
    == silver_customers["customer_city"].str.lower()
).all()

assert silver_customers["customer_state"].notna().all()
assert silver_customers.isna().sum().sum() == 0
assert invalid_states == set()

print("\nCustomers Silver validation passed.")
print(f"Rows: {len(silver_customers):,}")
print(f"Columns: {len(silver_customers.columns)}")


# ------------------------------------------------------------
# 2.6 Additional Customer Diagnostics
# ------------------------------------------------------------

character_counts = (
    silver_customers["customer_city"]
    .dropna()
    .astype(str)
    .str.cat(sep="")
)

character_counts = (
    pd.Series(list(character_counts))
    .value_counts()
    .sort_index()
)

for character, count in character_counts.items():
    display_character = (
        "<SPACE>" if character == " " else character
    )
    print(f"{display_character}: {count}")


length_analysis = []

for column in silver_customers.columns:
    values = (
        silver_customers[column]
        .dropna()
        .astype(str)
    )

    lengths = values.str.len()

    length_analysis.append({
        "column": column,
        "data_type": str(
            silver_customers[column].dtype
        ),
        "min_length": lengths.min(),
        "max_length": lengths.max(),
        "shortest_value": values.loc[lengths.idxmin()],
        "longest_value": values.loc[lengths.idxmax()]
    })

length_analysis = pd.DataFrame(length_analysis)

print("\nCustomer column length analysis:")
print(length_analysis.to_string(index=False))


# ============================================================
# 3. ORDERS – SILVER PREPROCESSING
# ============================================================

print("\n" + "=" * 60)
print("ORDERS – SILVER PREPROCESSING")
print("=" * 60)


# ------------------------------------------------------------
# 3.1 Data Audit & Key Validation
# ------------------------------------------------------------

print("Shape:", bronze_orders.shape)
print("\nColumns:")
print(bronze_orders.columns.tolist())

print("\nData types:")
print(bronze_orders.dtypes)

print("\nMissing values:")
orders_missing = (
    bronze_orders
    .isna()
    .sum()
    .sort_values(ascending=False)
    .to_frame("missing_count")
    .assign(
        missing_pct=lambda x: (
            x["missing_count"]
            / len(bronze_orders)
            * 100
        ).round(2)
    )
)

print(orders_missing.to_string())

print(
    "\nDuplicate rows:",
    bronze_orders.duplicated().sum()
)

print(
    "\nUnique order_ids:",
    bronze_orders["order_id"].nunique()
)

print("Total rows:", len(bronze_orders))

print(
    "Duplicate order_ids:",
    bronze_orders["order_id"].duplicated().sum()
)

customer_id_match = bronze_orders["customer_id"].isin(
    bronze_customers["customer_id"]
)

print(
    "Orders with valid customer_id:",
    customer_id_match.sum()
)

print(
    "Orders with missing customer reference:",
    (~customer_id_match).sum()
)

print("\nOrder status distribution:")

order_status_distribution = (
    bronze_orders["order_status"]
    .value_counts()
    .to_frame("order_count")
    .assign(
        percentage=lambda x: (
            x["order_count"]
            / len(bronze_orders)
            * 100
        ).round(2)
    )
)

print(order_status_distribution.to_string())


# ------------------------------------------------------------
# 3.2 Temporal Validation & Quality Flags
# ------------------------------------------------------------

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

bronze_orders[date_columns] = (
    bronze_orders[date_columns]
    .apply(pd.to_datetime)
)

print(
    "Approved before purchase:",
    (
        bronze_orders["order_approved_at"]
        < bronze_orders["order_purchase_timestamp"]
    ).sum()
)

print(
    "Carrier before purchase:",
    (
        bronze_orders["order_delivered_carrier_date"]
        < bronze_orders["order_purchase_timestamp"]
    ).sum()
)

print(
    "Customer delivery before purchase:",
    (
        bronze_orders["order_delivered_customer_date"]
        < bronze_orders["order_purchase_timestamp"]
    ).sum()
)

print(
    "Customer delivery before carrier:",
    (
        bronze_orders["order_delivered_customer_date"]
        < bronze_orders["order_delivered_carrier_date"]
    ).sum()
)


missing_pct_by_status = (
    bronze_orders
    .groupby("order_status")[date_columns]
    .apply(lambda x: x.isna().mean() * 100)
    .round(2)
)

print("\nMissing timestamp percentage by order status:")
print(missing_pct_by_status.to_string())

delivered_missing_dates = bronze_orders[
    (bronze_orders["order_status"] == "delivered")
    & bronze_orders[date_columns].isna().any(axis=1)
].copy()

print(
    "\nDelivered orders with missing timestamps:",
    len(delivered_missing_dates)
)

print(
    delivered_missing_dates[
        ["order_id", "order_status"] + date_columns
    ].head(5).to_string(index=False)
)


# Create temporal quality flags
bronze_orders["carrier_before_purchase_flag"] = (
    bronze_orders["order_delivered_carrier_date"]
    < bronze_orders["order_purchase_timestamp"]
)

bronze_orders["delivery_before_carrier_flag"] = (
    bronze_orders["order_delivered_customer_date"]
    < bronze_orders["order_delivered_carrier_date"]
)

# Create missing timestamp flags
bronze_orders["missing_approval_flag"] = (
    bronze_orders["order_approved_at"].isna()
)

bronze_orders["missing_carrier_date_flag"] = (
    bronze_orders["order_delivered_carrier_date"].isna()
)

bronze_orders["missing_delivery_date_flag"] = (
    bronze_orders["order_delivered_customer_date"].isna()
)

quality_flags = [
    "carrier_before_purchase_flag",
    "delivery_before_carrier_flag",
    "missing_approval_flag",
    "missing_carrier_date_flag",
    "missing_delivery_date_flag"
]

quality_flag_summary = pd.DataFrame({
    "flag": quality_flags,
    "count": [
        bronze_orders[column].sum()
        for column in quality_flags
    ]
})

quality_flag_summary["percentage"] = (
    quality_flag_summary["count"]
    / len(bronze_orders)
    * 100
).round(3)

print("\nOrders quality flag summary:")
print(quality_flag_summary.to_string(index=False))


# ------------------------------------------------------------
# 3.3 Customer Mapping
# ------------------------------------------------------------

# Map customer_unique_id from the validated
# Silver Customers dataset
customer_mapping = silver_customers[
    ["customer_id", "customer_unique_id"]
].copy()

assert customer_mapping["customer_id"].is_unique

bronze_orders = bronze_orders.merge(
    customer_mapping,
    on="customer_id",
    how="left",
    validate="many_to_one"
)

assert len(bronze_orders) == orders_raw_row_count
assert bronze_orders["customer_unique_id"].notna().all()

print("\nCustomer mapping validation passed.")
print(
    "Orders with customer_unique_id: "
    f"{bronze_orders['customer_unique_id'].notna().sum():,}"
)


# ------------------------------------------------------------
# 3.4 Create Silver Orders Dataset
# ------------------------------------------------------------

silver_orders = bronze_orders.copy()

silver_orders.insert(
    0,
    "id_orders",
    range(1, len(silver_orders) + 1)
)

expected_orders_columns = [
    "id_orders",
    "order_id",
    "customer_id",
    "customer_unique_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "carrier_before_purchase_flag",
    "delivery_before_carrier_flag",
    "missing_approval_flag",
    "missing_carrier_date_flag",
    "missing_delivery_date_flag"
]

silver_orders = silver_orders[
    expected_orders_columns
]

print(f"Rows: {len(silver_orders):,}")
print(f"Columns: {len(silver_orders.columns):,}")
print(
    "Unique id_orders:",
    silver_orders["id_orders"].nunique()
)


# ------------------------------------------------------------
# 3.5 Orders – Silver Data Quality Validation
# ------------------------------------------------------------

assert (
    silver_orders.columns.tolist()
    == expected_orders_columns
)

assert len(silver_orders) == orders_raw_row_count

assert silver_orders["id_orders"].notna().all()
assert silver_orders["id_orders"].is_unique
assert silver_orders["id_orders"].min() == 1
assert silver_orders["id_orders"].max() == len(
    silver_orders
)

assert silver_orders["order_id"].notna().all()
assert silver_orders["order_id"].is_unique
assert silver_orders["customer_id"].notna().all()
assert silver_orders["customer_unique_id"].notna().all()
assert silver_orders["order_status"].notna().all()
assert silver_orders["order_purchase_timestamp"].notna().all()

assert all(
    pd.api.types.is_datetime64_any_dtype(
        silver_orders[column]
    )
    for column in date_columns
)

assert all(
    silver_orders[column].dtype == bool
    for column in quality_flags
)

assert (
    silver_orders["carrier_before_purchase_flag"]
    == (
        silver_orders["order_delivered_carrier_date"]
        < silver_orders["order_purchase_timestamp"]
    )
).all()

assert (
    silver_orders["delivery_before_carrier_flag"]
    == (
        silver_orders["order_delivered_customer_date"]
        < silver_orders["order_delivered_carrier_date"]
    )
).all()

assert (
    silver_orders["missing_approval_flag"]
    == silver_orders["order_approved_at"].isna()
).all()

assert (
    silver_orders["missing_carrier_date_flag"]
    == silver_orders["order_delivered_carrier_date"].isna()
).all()

assert (
    silver_orders["missing_delivery_date_flag"]
    == silver_orders["order_delivered_customer_date"].isna()
).all()

silver_quality_summary = (
    silver_orders[quality_flags]
    .sum()
    .to_frame("flagged_count")
)

silver_quality_summary["flagged_pct"] = (
    silver_quality_summary["flagged_count"]
    / len(silver_orders)
    * 100
).round(3)

print("\nOrders Silver validation passed.")
print(f"Rows: {len(silver_orders):,}")
print(
    "Unique order_ids:",
    silver_orders["order_id"].nunique()
)


# ------------------------------------------------------------
# 3.6 Order Status Diagnostics
# ------------------------------------------------------------

character_counts = (
    silver_orders["order_status"]
    .dropna()
    .astype(str)
    .str.cat(sep="")
)

character_counts = (
    pd.Series(list(character_counts))
    .value_counts()
    .sort_index()
)

for character, count in character_counts.items():
    display_character = (
        "<SPACE>" if character == " " else character
    )
    print(f"{display_character}: {count}")

order_status_counts = (
    silver_orders["order_status"]
    .value_counts(dropna=False)
    .rename_axis("order_status")
    .reset_index(name="count")
)

print("\nOrder status counts:")
print(order_status_counts.to_string(index=False))


# ============================================================
# 4. ORDER REVIEWS – SILVER PREPROCESSING
# ============================================================

print("\n" + "=" * 60)
print("ORDER REVIEWS – SILVER PREPROCESSING")
print("=" * 60)


# ------------------------------------------------------------
# 4.1 Data Understanding & Quality Assessment
# ------------------------------------------------------------

print("Shape:", bronze_order_reviews.shape)
print("\nColumns:")
print(bronze_order_reviews.columns.tolist())

print("\nData types:")
print(bronze_order_reviews.dtypes)

print("\nMissing values:")

review_missing = (
    bronze_order_reviews
    .isna()
    .sum()
    .to_frame("missing_count")
    .assign(
        missing_pct=lambda x: (
            x["missing_count"]
            / len(bronze_order_reviews)
            * 100
        )
    )
)

print(review_missing.to_string())

print(
    "\nDuplicate rows:",
    bronze_order_reviews.duplicated().sum()
)

print(
    "Unique review_id:",
    bronze_order_reviews["review_id"].nunique()
)

print(
    "Rows with duplicated review_id:",
    bronze_order_reviews["review_id"].duplicated().sum()
)

print(
    "Unique order_id:",
    bronze_order_reviews["order_id"].nunique()
)

print(
    "Rows with duplicated order_id:",
    bronze_order_reviews["order_id"].duplicated().sum()
)

print("\nReview score distribution:")
print(
    bronze_order_reviews["review_score"]
    .value_counts()
    .sort_index()
)


# ------------------------------------------------------------
# 4.2 Review Input Validation
# ------------------------------------------------------------

expected_review_input_columns = [
    "review_id",
    "order_id",
    "review_score",
    "review_comment_title",
    "review_comment_title_en",
    "review_comment_message",
    "review_comment_message_en",
    "review_creation_date",
    "review_answer_timestamp"
]

assert (
    bronze_order_reviews.columns.tolist()
    == expected_review_input_columns
)

mandatory_review_columns = [
    "review_id",
    "order_id",
    "review_score",
    "review_creation_date",
    "review_answer_timestamp"
]

assert (
    bronze_order_reviews[mandatory_review_columns]
    .notna()
    .all()
    .all()
)

assert (
    bronze_order_reviews["review_score"]
    .between(1, 5)
    .all()
)

review_creation_dt = pd.to_datetime(
    bronze_order_reviews["review_creation_date"],
    errors="coerce"
)

review_answer_dt = pd.to_datetime(
    bronze_order_reviews["review_answer_timestamp"],
    errors="coerce"
)

assert review_creation_dt.notna().all()
assert review_answer_dt.notna().all()

answer_before_creation = (
    review_answer_dt < review_creation_dt
)

assert not answer_before_creation.any()

print("\nOrder Reviews Bronze validation passed.")


# ------------------------------------------------------------
# 4.3 Create Silver Dataset & Normalize Text
# ------------------------------------------------------------

silver_order_reviews = bronze_order_reviews.copy()

silver_order_reviews["id_order_reviews"] = range(
    1,
    len(silver_order_reviews) + 1
)

silver_order_reviews.insert(
    0,
    "id_order_reviews",
    silver_order_reviews.pop("id_order_reviews")
)

assert silver_order_reviews["id_order_reviews"].is_unique
assert silver_order_reviews["id_order_reviews"].min() == 1
assert (
    silver_order_reviews["id_order_reviews"].max()
    == len(silver_order_reviews)
)

comment_columns = [
    "review_comment_title",
    "review_comment_message"
]

for column in comment_columns:
    silver_order_reviews[column] = (
        silver_order_reviews[column]
        .astype("string")
        .str.lower()
        .str.replace(
            r"[^a-z\s.,!?]",
            "",
            regex=True
        )
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
        .str.strip()
        .replace("", pd.NA)
    )

translation_columns = [
    "review_comment_title_en",
    "review_comment_message_en"
]

for column in translation_columns:
    silver_order_reviews[column] = (
        silver_order_reviews[column]
        .astype("string")
        .str.lower()
        .str.replace(
            r"[^a-z\s.,!?]",
            "",
            regex=True
        )
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
        .str.strip()
        .replace("", pd.NA)
    )


# ------------------------------------------------------------
# 4.4 Complete Defined English Translation Mappings
# ------------------------------------------------------------

silver_order_reviews.loc[
    silver_order_reviews["review_comment_title"]
    == "nota dez",
    "review_comment_title_en"
] = "ranking ten"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_title"]
    == "nota",
    "review_comment_title_en"
] = "ranking"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_message"]
    == "nota",
    "review_comment_message_en"
] = "ranking"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_title"]
    == "nenhuma",
    "review_comment_title_en"
] = "none"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_message"]
    == "nenhuma",
    "review_comment_message_en"
] = "none"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_message"]
    == "nd",
    "review_comment_message_en"
] = "not available"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_message"]
    == "no h",
    "review_comment_message_en"
] = "there is no"


# ------------------------------------------------------------
# 4.5 Validate Normalized Text Fields
# ------------------------------------------------------------

for column in comment_columns + translation_columns:
    non_null_values = (
        silver_order_reviews[column]
        .dropna()
    )

    assert (
        non_null_values
        == non_null_values.str.strip()
    ).all()

    assert (
        non_null_values
        == non_null_values.str.lower()
    ).all()

    assert (
        non_null_values
        .str.match(r"^[a-z\s.,!?]+$")
        .all()
    )

assert (
    silver_order_reviews["review_comment_title"].isna()
    == silver_order_reviews["review_comment_title_en"].isna()
).all()

assert (
    silver_order_reviews["review_comment_message"].isna()
    == silver_order_reviews["review_comment_message_en"].isna()
).all()


# ------------------------------------------------------------
# 4.6 Datetime Transformation & Validation
# ------------------------------------------------------------

datetime_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in datetime_columns:
    silver_order_reviews[column] = pd.to_datetime(
        silver_order_reviews[column],
        errors="raise"
    )

assert (
    silver_order_reviews[datetime_columns]
    .notna()
    .all()
    .all()
)

answer_before_creation = (
    silver_order_reviews["review_answer_timestamp"]
    < silver_order_reviews["review_creation_date"]
)

assert not answer_before_creation.any()

assert (
    len(silver_order_reviews)
    == len(bronze_order_reviews)
)

assert (
    silver_order_reviews["review_id"].nunique()
    == bronze_order_reviews["review_id"].nunique()
)

assert (
    silver_order_reviews["order_id"].nunique()
    == bronze_order_reviews["order_id"].nunique()
)

print(
    "\nOrder Reviews transformation validation passed."
)


# ------------------------------------------------------------
# 4.7 Order Reviews – Silver Data Quality Validation
# ------------------------------------------------------------

expected_order_reviews_columns = [
    "id_order_reviews",
    "review_id",
    "order_id",
    "review_score",
    "review_comment_title",
    "review_comment_title_en",
    "review_comment_message",
    "review_comment_message_en",
    "review_creation_date",
    "review_answer_timestamp"
]

assert (
    silver_order_reviews.columns.tolist()
    == expected_order_reviews_columns
)

assert (
    len(silver_order_reviews)
    == order_reviews_raw_row_count
)

assert silver_order_reviews["id_order_reviews"].notna().all()
assert silver_order_reviews["id_order_reviews"].is_unique
assert silver_order_reviews["id_order_reviews"].min() == 1
assert (
    silver_order_reviews["id_order_reviews"].max()
    == len(silver_order_reviews)
)

assert (
    silver_order_reviews[mandatory_review_columns]
    .notna()
    .all()
    .all()
)

assert (
    silver_order_reviews["review_score"]
    .between(1, 5)
    .all()
)

assert (
    silver_order_reviews["review_comment_title"].isna()
    == silver_order_reviews["review_comment_title_en"].isna()
).all()

assert (
    silver_order_reviews["review_comment_message"].isna()
    == silver_order_reviews["review_comment_message_en"].isna()
).all()

assert pd.api.types.is_datetime64_any_dtype(
    silver_order_reviews["review_creation_date"]
)

assert pd.api.types.is_datetime64_any_dtype(
    silver_order_reviews["review_answer_timestamp"]
)

assert (
    silver_order_reviews["review_answer_timestamp"]
    >= silver_order_reviews["review_creation_date"]
).all()

print("\nOrder Reviews Silver validation passed.")
print(
    f"Rows: {len(silver_order_reviews):,}"
)
print(
    f"Columns: {len(silver_order_reviews.columns):,}"
)


# ------------------------------------------------------------
# 4.8 Order Reviews Character Diagnostics
# ------------------------------------------------------------

columns_to_check = [
    "review_comment_title",
    "review_comment_title_en",
    "review_comment_message",
    "review_comment_message_en",
    "review_score"
]

for column in columns_to_check:
    print(f"\n--- {column} ---")

    character_counts = (
        silver_order_reviews[column]
        .dropna()
        .astype(str)
        .str.cat(sep="")
    )

    character_counts = (
        pd.Series(list(character_counts))
        .value_counts()
        .sort_index()
    )

    for character, count in character_counts.items():
        display_character = (
            "<SPACE>" if character == " "
            else character
        )

        print(
            f"{display_character}: {count}"
        )


# ============================================================
# 5. FINAL CROSS-DATASET VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL SILVER VALIDATION")
print("=" * 60)


assert len(silver_customers) == customers_raw_row_count
assert len(silver_orders) == orders_raw_row_count
assert (
    len(silver_order_reviews)
    == order_reviews_raw_row_count
)

assert silver_customers["customer_id"].is_unique
assert silver_orders["order_id"].is_unique
assert silver_order_reviews["id_order_reviews"].is_unique

# Orders must be fully mapped to validated Silver Customers
assert (
    silver_orders["customer_unique_id"]
    .notna()
    .all()
)

print(
    "All three Silver datasets passed the "
    "final cross-dataset validation."
)


# ============================================================
# 6. LOCAL SILVER EXPORT
# ============================================================
#
# This block is intentionally inactive.
# It is used for local testing only.
#
# ------------------------------------------------------------

# customers_output = (
#     PROCESSED_PATH / "silver_customers.csv"
# )

# orders_output = (
#     PROCESSED_PATH / "silver_orders.csv"
# )

# order_reviews_output = (
#     PROCESSED_PATH / "silver_order_reviews_en.csv"
# )


# silver_customers.to_csv(
#     customers_output,
#     index=False
# )

# silver_orders.to_csv(
#     orders_output,
#     index=False
# )

# silver_order_reviews.to_csv(
#     order_reviews_output,
#     index=False
# )


# print("Silver datasets exported successfully:")
# print(f"- Customers: {customers_output}")
# print(f"- Orders: {orders_output}")
# print(f"- Order Reviews: {order_reviews_output}")


# ============================================================
# 7. S3 SILVER EXPORT – AWS LAMBDA VERSION
# ============================================================
#
# This block is intentionally inactive.
# It is used when AWS Lambda exports the Silver datasets
# directly to S3.
#
# ------------------------------------------------------------

# import boto3
# from io import StringIO


# S3_BUCKET = (
#     "dsi-final-project-360964564955-eu-central-1-an"
# )

# PROCESSED_PREFIX = "processed/"


# s3 = boto3.client("s3")


# def save_csv_to_s3(df, bucket, key):
#     """
#     Upload a pandas DataFrame to S3 as a CSV file.
#     """

#     csv_buffer = StringIO()

#     df.to_csv(
#         csv_buffer,
#         index=False
#     )

#     s3.put_object(
#         Bucket=bucket,
#         Key=key,
#         Body=csv_buffer.getvalue(),
#         ContentType="text/csv"
#     )

#     print(
#         f"Successfully uploaded: "
#         f"s3://{bucket}/{key}"
#     )


# save_csv_to_s3(
#     silver_customers,
#     S3_BUCKET,
#     f"{PROCESSED_PREFIX}silver_customers.csv"
# )

# save_csv_to_s3(
#     silver_orders,
#     S3_BUCKET,
#     f"{PROCESSED_PREFIX}silver_orders.csv"
# )

# save_csv_to_s3(
#     silver_order_reviews,
#     S3_BUCKET,
#     f"{PROCESSED_PREFIX}silver_order_reviews_en.csv"
# )

# print(
#     "All Silver datasets successfully exported to S3."
# )


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("SILVER PREPROCESSING COMPLETED")
print("=" * 60)

print(
    f"silver_customers: "
    f"{silver_customers.shape}"
)

print(
    f"silver_orders: "
    f"{silver_orders.shape}"
)

print(
    f"silver_order_reviews: "
    f"{silver_order_reviews.shape}"
)

print("\nAvailable Silver DataFrames:")
print("- silver_customers")
print("- silver_orders")
print("- silver_order_reviews")

################################################################
# End Code David
################################################################