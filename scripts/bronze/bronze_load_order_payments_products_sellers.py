import pandas as pd
import os


current_layer = "bronze"
source_type = ".csv"
seperator = ","
source_path = "./datasets/raw/"
destination_path = f"./scripts/{current_layer}/"
destination_type = ".pkl"

source_tables_dict = {
    "order_payments": "olist_order_payments_dataset",
    "products": "olist_products_dataset",
    "sellers": "olist_sellers_dataset"
}

source_tables_list = []

pickle_dict = {}

# load data in structure [current_layer][source][tablename]

for key, value in source_tables_dict.items():

    table_name = current_layer + source_type + "_" + key + source_type
    dataframe_name = table_name
    dataframe_name = pd.read_csv(source_path + value + source_type, sep=seperator)
    pickle_dict[table_name] = dataframe_name
    source_tables_list.append(table_name)

print(f"Successfully loaded {source_tables_list} in {current_layer}-Layer")

pd.to_pickle(pickle_dict, f"{destination_path}{current_layer}_tables{destination_type}")

print(f"Successfully saved as {destination_type} in {destination_path}")