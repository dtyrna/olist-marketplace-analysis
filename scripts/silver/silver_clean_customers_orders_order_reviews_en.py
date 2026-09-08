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
# 3.3 Create Silver Orders Dataset
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
# 3.4 Orders – Silver Data Quality Validation
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
# 3.5 Order Status Diagnostics
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