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

for col in numeric_columns:

    try:
        df_order_payments[col] = pd.to_numeric(df_order_payments[col], errors="raise")
        print(f"{col} successfully converted into {df_order_payments[col].dtype}")
        
    except Execution as e:
        print(f"Error in converting {col} into numeric")
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

for col in numeric_columns:

    try:
        df_products[col] = pd.to_numeric(df_products[col], errors="raise")
        print(f"{col} successfully converted into {df_products[col].dtype}")
        
    except Execution as e:
        print(f"Error in converting {col} into numeric")
        print(f"Error details: {e}")
        sys.exit(1) #exit script to avoid errors

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