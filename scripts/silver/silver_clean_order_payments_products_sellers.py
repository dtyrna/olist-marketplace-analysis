import pandas as pd

last_layer = "bronze"
current_layer = "silver"
source_path = f"./scripts/{last_layer}/"
source_type = ".pkl"


bronze_tables_dict = pd.read_pickle(f"{source_path}{last_layer}_tables{source_type}")

print(f"Pickle Tables ({", ".join(bronze_tables_dict.keys())}) successsfully loaded into {current_layer}-Layer!")

