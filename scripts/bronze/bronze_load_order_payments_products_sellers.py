import pandas as pd
import os


layer = "bronze"
source_type = ".csv"
seperator = ","
source_path = "./datasets/raw/"
destination_path = f"./scripts/{layer}/"

source_tables_dict = {
    "order_payments": "olist_order_payments_dataset",
    "products": "olist_products_dataset",
    "sellers": "olist_sellers_dataset"
}

source_tables_list = []

pickle_dict = {}

# load data in structure [layer][source][tablename]

for key, value in source_tables_dict.items():

    tablename = layer + source_type + key + source_type
    dataframe_name = tablename
    dataframe_name = pd.read_csv(source_path + value + source_type, sep=seperator)
    pickle_dict[tablename] = dataframe_name
    source_tables_list.append(value+source_type)

print(f"Successfully loaded {source_tables_list} in {layer}-Layer")

pd.to_pickle(pickle_dict, destination_path + "bronze_tables" + ".pkl")
