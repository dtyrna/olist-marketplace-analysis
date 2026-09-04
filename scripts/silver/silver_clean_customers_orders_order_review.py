"""
Olist Marketplace – Silver Cleaning
Customers, Orders & Order Reviews

Converted from the combined Silver preprocessing notebook.

IMPORTANT:
- Data import/load operations are intentionally commented out.
- Data export operations are intentionally commented out.
- The preprocessing, validation, and transformation logic remains visible.
- Activate exactly one input strategy (local or S3) and one output strategy
  when the team decides on the final execution environment.
"""


# ====================================================================
# Olist Marketplace – Silver Cleaning
# Customers, Orders & Order Reviews
# This notebook combines the three existing preprocessing notebooks for the Silver Layer:
# 1. **Customers**
# 2. **Orders**
# 3. **Order Reviews**
# The three sections remain clearly separated both conceptually and within the notebook.
# The setup, path definitions, and loading of the Bronze datasets are performed **only once**.
# The existing cleaning and validation logic of the three individual notebooks is retained. At the end, all three validated Silver datasets are exported together to the `processed` folder.
# ====================================================================


# ====================================================================
# Common Setup & Bronze Data Load
# ====================================================================

import pandas as pd
import numpy as np
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

RAW_PATH = Path("../datasets/raw")
PROCESSED_PATH = Path("../datasets/processed")

PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# CURRENT LOCAL DATA IMPORT – INTENTIONALLY COMMENTED OUT
# ------------------------------------------------------------
# # Load all Bronze datasets once
#
# bronze_customers = pd.read_csv(
#     RAW_PATH / "olist_customers_dataset.csv"
# )
#
# bronze_orders = pd.read_csv(
#     RAW_PATH / "olist_orders_dataset.csv"
# )
#
# bronze_order_reviews = pd.read_csv(
#     RAW_PATH / "olist_order_reviews_dataset_en.csv"
# )
#
# # Preserve raw row counts for later validation
# customers_raw_row_count = len(bronze_customers)
# orders_raw_row_count = len(bronze_orders)
# order_reviews_raw_row_count = len(bronze_order_reviews)
#
# print(f"Bronze customers: {bronze_customers.shape}")
# print(f"Bronze orders: {bronze_orders.shape}")
# print(f"Bronze order reviews: {bronze_order_reviews.shape}")


# ====================================================================
# S3 SETUP & BRONZE DATA LOAD – FUTURE LAMBDA VERSION
# This block is intentionally commented out.
# It will be activated when the preprocessing pipeline is moved from local processing to AWS Lambda.
# ====================================================================


# Data flow:
#
# S3 Bucket
#     └── raw/
#          ├── olist_customers_dataset.csv
#          ├── olist_orders_dataset.csv
#          └── olist_order_reviews_dataset.csv
#
#                 ↓
#
#              AWS Lambda
#
#                 ↓
#
# S3 Bucket
#     └── processed/
#          ├── silver_customers.csv
#          ├── silver_orders.csv
#          └── silver_order_reviews_en.csv
#
# ============================================================


# import boto3
# from io import StringIO


# ------------------------------------------------------------
# S3 Configuration
# ------------------------------------------------------------

# S3_BUCKET = "dsi-final-project-360964564955-eu-central-1-an"

# RAW_PREFIX = "raw/"
# PROCESSED_PREFIX = "processed/"


# ------------------------------------------------------------
# S3 Client
# ------------------------------------------------------------

# s3 = boto3.client("s3")


# ------------------------------------------------------------
# Load Bronze datasets from S3
# ------------------------------------------------------------

# def load_csv_from_s3(bucket, key):
#     response = s3.get_object(
#         Bucket=bucket,
#         Key=key
#     )
#
#     return pd.read_csv(response["Body"])


# bronze_customers = load_csv_from_s3(
#     S3_BUCKET,
#     f"{RAW_PREFIX}olist_customers_dataset.csv"
# )
#
# bronze_orders = load_csv_from_s3(
#     S3_BUCKET,
#     f"{RAW_PREFIX}olist_orders_dataset.csv"
# )
#
# bronze_order_reviews = load_csv_from_s3(
#     S3_BUCKET,
#     f"{RAW_PREFIX}olist_order_reviews_dataset_en.csv"
# )


# ------------------------------------------------------------
# Preserve raw row counts for later validation
# ------------------------------------------------------------

# customers_raw_row_count = len(bronze_customers)
# orders_raw_row_count = len(bronze_orders)
# order_reviews_raw_row_count = len(bronze_order_reviews)


# print(f"Bronze customers: {bronze_customers.shape}")
# print(f"Bronze orders: {bronze_orders.shape}")
# print(f"Bronze order reviews: {bronze_order_reviews.shape}")


# ====================================================================
# CUSTOMERS – Silver Preprocessing
# ---
# **Dataset:** `olist_customers_dataset.csv`
# **Silver output:** `silver_customers.csv`
# This section is structured independently from the other functional areas and uses the shared setup.
# ====================================================================


# ====================================================================
# 1. Data Audit
# The raw dataset is inspected before any transformation is applied.
# The audit covers:
# - dataset dimensions
# - column names
# - data types
# - missing values
# - duplicate records
# - key uniqueness
# - customer identifier cardinality
# - categorical values
# - ZIP code plausibility
# ====================================================================

#Check shape
bronze_customers.shape

#Check columns
bronze_customers.columns.tolist()

#Check datatypes
bronze_customers.info()

#Check missing values
bronze_customers.isna().sum()

bronze_customers.isna().mean().mul(100).round(2)

#Check duplicates
bronze_customers.duplicated().sum()

bronze_customers["customer_id"].nunique()

len(bronze_customers)

#Check primary keys
bronze_customers["customer_id"].is_unique

#Check unique ids
bronze_customers["customer_unique_id"].nunique()

customer_counts = (
    bronze_customers
    .groupby("customer_unique_id")
    .size()
    .sort_values(ascending=False))

customer_counts.head(10)

#How many unique customers have multiple customer records?
(customer_counts > 1).sum()

#How many customers have more than one record?
customer_counts.value_counts().sort_index()

repeat_customer_records = customer_counts[customer_counts > 1]

repeat_customer_records.describe()

repeat_customer_records.sum()


# ====================================================================
# Customer Record Cardinality
# The dataset contains 96,096 unique `customer_unique_id` values across
# 99,441 customer records.
# 2,997 customers have more than one customer record, accounting for
# 6,342 customer records in total.
# These repeated `customer_unique_id` values are not considered duplicate
# records because `customer_id` remains unique and represents the
# customer-record level of this table.
# ====================================================================

#Check customer state
bronze_customers["customer_state"].value_counts()

bronze_customers["customer_city"].nunique()

#Check zip-code
bronze_customers["customer_zip_code_prefix"].describe()

bronze_customers["customer_zip_code_prefix"].nunique()

(bronze_customers["customer_zip_code_prefix"] < 0).sum()

bronze_customers["customer_zip_code_prefix"].isna().sum()


# ====================================================================
# Audit Findings
# The raw customers dataset contains 99,441 records and 5 columns.
# No missing values were identified and no fully duplicated rows were found.
# `customer_id` is unique across all records and therefore represents the
# primary key at the customer-record level.
# `customer_unique_id` contains repeated values. This is expected because
# multiple customer records can belong to the same underlying customer.
# Therefore, `customer_unique_id` must not be treated as the primary key of
# this table.
# The dataset contains 27 state codes, 4,119 unique cities and 14,994 ZIP
# code prefixes.
# No structural data quality issue requiring record removal was identified
# ====================================================================


# ====================================================================
# 2. Cleaning & Standardization
# The raw dataset is preserved and all transformations are applied to a
# separate working copy.
# Because the audit identified no missing values, duplicate records or
# primary-key violations, no customer records are removed during
# preprocessing.
# The following transformations are applied:
# - remove leading and trailing whitespace from string fields
# - standardize state codes to uppercase
# - explicitly define data types
# - preserve the original city naming rather than applying aggressive
# text normalization
# ====================================================================

#Create copy
silver_customers = bronze_customers.copy()

# Create Silver Unique Key
silver_customers.insert(
    0,
    "id_customers",
    range(1, len(silver_customers) + 1)
)

#Check columns
silver_customers.columns.tolist()


# ====================================================================
# Silver Unique Key
# A technical unique key `id_customers` is created for the Silver table.
# The original source identifiers `customer_id` and `customer_unique_id` are retained unchanged.
# `id_customers` is generated as a sequential integer starting at 1 and serves as the technical unique identifier of each Silver record.
# ====================================================================

#Identifying string columns and removing spaces
string_columns = [
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state"]

for col in string_columns:
    silver_customers[col] = silver_customers[col].str.strip()

#Normalize 'state' and check
silver_customers["customer_state"] = (
   silver_customers["customer_state"].str.lower())

silver_customers["customer_state"].unique()

silver_customers["customer_state"].nunique()

#Normalize 'city'
silver_customers["customer_city"] = (
    silver_customers["customer_city"].str.strip())


# ====================================================================
# City Standardization Decision
# City values are only stripped of leading and trailing whitespace.
# No lower-case, title-case or character replacement is applied because
# aggressive normalization could alter geographic names or remove
# meaningful linguistic information.
# Further geographic standardization, if required, should be handled as a
# separate data-quality or geospatial transformation.
# ====================================================================

#Define datatypes
#IDs
silver_customers["customer_id"] = (
    silver_customers["customer_id"].astype("string"))

silver_customers["customer_unique_id"] = (
    silver_customers["customer_unique_id"].astype("string"))

#City
silver_customers["customer_city"] = (
    silver_customers["customer_city"].astype("string"))

#State
silver_customers["customer_state"] = (
    silver_customers["customer_state"].astype("string"))

#ZIP Prefix
silver_customers["customer_zip_code_prefix"] = (
    silver_customers["customer_zip_code_prefix"]
    .astype("string")
    .str.zfill(5))

#Check datatypes
silver_customers.dtypes

#Compare raw and cleaned dataset
print("Raw rows:", len(silver_customers))
print("Silver rows:", len(silver_customers))

assert len(silver_customers) == len(silver_customers)

#Check if new missing values appeared
silver_customers.isna().sum()

# Standardize city names:
# - convert to lowercase
# - replace hyphens with spaces
# - remove apostrophes
# - remove leading/trailing whitespace
# - normalize multiple spaces

silver_customers["customer_city"] = (
    silver_customers["customer_city"]
    .str.lower()
    .str.replace("-", " ", regex=False)
    .str.replace("'", "", regex=False)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# Replace incorrect city value
silver_customers.loc[
    silver_customers["customer_city"] == "quilometro 14 do mutum",
    "customer_city"
] = "mutum"

print(
    silver_customers.loc[
        silver_customers["customer_city"] == "mutum",
        "customer_city"
    ].value_counts()
)

#State quality check
valid_states = {
    'sp', 'sc', 'mg', 'pr', 'rj', 'rs', 'pa', 'go', 'es', 'ba', 'ma', 'ms', 'ce',
    'df', 'rn', 'pe', 'mt', 'am', 'ap', 'al', 'ro', 'pb', 'to', 'pi', 'ac', 'se',
    'rr'
}

invalid_states = set(silver_customers["customer_state"].dropna().unique()) - valid_states

invalid_states

#ZIP Prefix quality check

silver_customers["customer_zip_code_prefix"].str.len().eq(5).all()
silver_customers["customer_zip_code_prefix"].str.isnumeric().all()

#Primary-Key quality check
assert silver_customers["customer_id"].notna().all()

assert silver_customers["customer_id"].is_unique


# ====================================================================
# 3. Silver Data Quality Validation Customers
# Before exporting the Silver dataset, a quality gate is applied.
# The Silver dataset must satisfy the following requirements:
# - record count remains unchanged
# - `customer_id` is non-null
# - `customer_id` is unique
# - `customer_unique_id` is non-null
# - `customer_state` is non-null
# - no missing values remain
# - all state codes are valid
# - ZIP code prefixes fall within the defined plausibility range
# ====================================================================

expected_columns = [
    "id_customers",
    "customer_id",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state"
]

assert silver_customers.columns.tolist() == expected_columns

assert len(silver_customers) == len(bronze_customers)

assert silver_customers["id_customers"].notna().all()
assert silver_customers["id_customers"].is_unique
assert silver_customers["id_customers"].min() == 1
assert silver_customers["id_customers"].max() == len(silver_customers)

assert silver_customers["customer_id"].notna().all()
assert silver_customers["customer_id"].is_unique

assert silver_customers["customer_unique_id"].notna().all()

assert silver_customers["customer_city"].str.match(r"^[a-z\s]+$").all()

assert (silver_customers["customer_city"]== silver_customers["customer_city"].str.lower()).all()

assert silver_customers["customer_state"].notna().all()

assert silver_customers.isna().sum().sum() == 0

assert invalid_states == set()

assert silver_customers["customer_zip_code_prefix"].str.len().eq(5).all()
assert silver_customers["customer_zip_code_prefix"].str.isnumeric().all()

print("Silver data quality checks passed successfully.")


# ====================================================================
# 4. Customers - Preprocessing Summary
# The customers dataset successfully passed the preprocessing quality gate.
# Result
# - 99,441 customer records retained
# - no records removed
# - no missing values identified
# - `id_customers` integrated and validated as unique key
# - `customer_unique_id` correctly treated as the underlying customer identifier
# - `customer_id` validated as the primary key at customer-record level
# - state codes validated
# - string fields standardized
# - data types explicitly defined
# The Silver customer dataset is now ready to be used as an input for
# downstream analysis and integration with the orders dataset.
# ====================================================================


# ====================================================================
# ORDERS – Silver Preprocessing
# ---
# **Dataset:** `olist_orders_dataset.csv`
# **Silver output:** `silver_orders.csv`
# This section uses `bronze_customers`, which was already loaded in the shared setup.
# ====================================================================


print("Shape:", bronze_orders.shape)
print("\nColumns:")
print(bronze_orders.columns.tolist())

print("\nData types:")
print(bronze_orders.dtypes)

print("\nFirst rows:")
display(bronze_orders.head())

print("\nMissing values:")
display(
    bronze_orders.isna()
    .sum()
    .sort_values(ascending=False)
    .to_frame("missing_count")
    .assign(
        missing_pct=lambda x: (x["missing_count"] / len(bronze_orders) * 100).round(2)
    )
)

print("\nDuplicate rows:", bronze_orders.duplicated().sum())


# ====================================================================
# 1. Data Quality & Key Validation
# Validate primary key uniqueness, customer references and order status values.
# ====================================================================


# ====================================================================
# Key Integrity
# Validate the uniqueness of the order primary key and identify duplicate order records.
# Key Definition
# The `orders` dataset uses the following key structure:
# - `id_orders`: technical surrogate key of the Silver layer, generated sequentially starting at 1.
# - `order_id`: business/natural key identifying the original Olist order.
# - `customer_id`: foreign key referencing `customer_id` in the customers dataset.
# The surrogate key is introduced in the Silver layer, while the original `order_id` is preserved as the business key.
# ====================================================================

# Validate primary key uniqueness

print("Unique order_ids:", bronze_orders["order_id"].nunique())
print("Total rows:", len(bronze_orders))
print("Duplicate order_ids:", bronze_orders["order_id"].duplicated().sum())

customer_id_match = bronze_orders["customer_id"].isin(bronze_customers["customer_id"])

print("Orders with valid customer_id:", customer_id_match.sum())
print("Orders with missing customer reference:", (~customer_id_match).sum())


# ====================================================================
# Order Status Distribution
# Examine the distribution of order statuses to understand the composition of the order dataset and identify dominant order lifecycle stages.
# ====================================================================

print("Order status distribution:")
display(
    bronze_orders["order_status"]
    .value_counts()
    .to_frame("order_count")
    .assign(percentage=lambda x: (x["order_count"] / len(bronze_orders) * 100).round(2)))


# ====================================================================
# Temporal Consistency
# Validate the logical sequence of order events and identify records with impossible timestamp relationships.
# Temporal Fields Preparation
# Convert order lifecycle timestamps to datetime format before validating their temporal consistency.
# ====================================================================

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"]

bronze_orders[date_columns] = bronze_orders[date_columns].apply(pd.to_datetime)

bronze_orders[date_columns].dtypes

print("Approved before purchase:",(bronze_orders["order_approved_at"] < bronze_orders["order_purchase_timestamp"]).sum())

print("Carrier before purchase:",(bronze_orders["order_delivered_carrier_date"] < bronze_orders["order_purchase_timestamp"]).sum())

print("Customer delivery before purchase:",(bronze_orders["order_delivered_customer_date"] < bronze_orders["order_purchase_timestamp"]).sum())

print("Customer delivery before carrier:",(bronze_orders["order_delivered_customer_date"]< bronze_orders["order_delivered_carrier_date"]).sum())

# Missing timestamp rates by order status

missing_pct_by_status = (bronze_orders.groupby("order_status")[date_columns].apply(lambda x: x.isna().mean() * 100).round(2))

display(missing_pct_by_status)


# ====================================================================
# Temporal Anomaly Assessment
# Quantify the magnitude of temporal inconsistencies to distinguish isolated data-quality issues from potentially systematic problems.
# ====================================================================

# Assess magnitude of temporal anomalies

# Carrier date before purchase
carrier_anomalies = bronze_orders.loc[
    bronze_orders["order_delivered_carrier_date"]
    < bronze_orders["order_purchase_timestamp"]
].copy()

carrier_anomalies["difference_minutes"] = (
    carrier_anomalies["order_purchase_timestamp"]
    - carrier_anomalies["order_delivered_carrier_date"]
).dt.total_seconds() / 60


# Customer delivery before carrier
delivery_anomalies = bronze_orders.loc[
    bronze_orders["order_delivered_customer_date"]
    < bronze_orders["order_delivered_carrier_date"]
].copy()

delivery_anomalies["difference_minutes"] = (
    delivery_anomalies["order_delivered_carrier_date"]
    - delivery_anomalies["order_delivered_customer_date"]
).dt.total_seconds() / 60


# Summarize anomaly magnitude
print("Carrier before purchase:")
display(
    carrier_anomalies["difference_minutes"].describe()
)

print("\nDelivery before carrier:")
display(
    delivery_anomalies["difference_minutes"].describe()
)

# Review most extreme temporal anomalies

print("Carrier before purchase - largest deviations:")
display(
    carrier_anomalies[
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_carrier_date",
            "difference_minutes"
        ]
    ]
    .sort_values("difference_minutes", ascending=False)
    .head(5)
)

print("\nDelivery before carrier - largest deviations:")
display(
    delivery_anomalies[
        [
            "order_id",
            "order_status",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "difference_minutes"
        ]
    ]
    .sort_values("difference_minutes", ascending=False)
    .head(5)
)


# ====================================================================
# Data Quality Decision
# Temporal inconsistencies affect a small number of records. Since the correct timestamps cannot be reliably inferred, the original values are retained.
# Affected records are flagged and excluded from derived duration calculations where the affected timestamp is required.
# ====================================================================


# ====================================================================
# Missing Value Assessment & Treatment
# Missing timestamps are largely consistent with the respective order status. For example, delivery-related timestamps are naturally absent for orders that have not reached the delivery stage.
# A small number of delivered orders also contain missing timestamps. Since the correct event times cannot be reliably inferred, missing values are retained as `NaN` and no imputation or row deletion is performed.
# ====================================================================

# Missing values by order status and date column

missing_pct_by_status = (
    bronze_orders
    .groupby("order_status")[date_columns]
    .apply(lambda x: x.isna().mean() * 100)
    .round(2))

display(missing_pct_by_status)

# Investigate missing timestamps in delivered orders

delivered_missing_dates = bronze_orders[
    (bronze_orders["order_status"] == "delivered")
    & (
        bronze_orders[date_columns]
        .isna()
        .any(axis=1)
    )
].copy()

print("Delivered orders with missing timestamps:",len(delivered_missing_dates))

display(delivered_missing_dates[["order_id", "order_status"] + date_columns].head(5))


# ====================================================================
# Data Quality Summary
# The order data is suitable for further analysis after applying explicit quality flags. Temporal inconsistencies are retained in the original data but excluded from affected duration calculations. Missing timestamps are retained as `NaN` where no reliable imputation is possible.
# The resulting dataset preserves the original observations while preventing identified data-quality issues from distorting derived analytical features.
# ====================================================================


# ====================================================================
# 2. Temporal Quality Flags
# Create flags for temporal inconsistencies without modifying the original timestamp columns.
# ====================================================================


# ====================================================================
# Temporal anomaly flags
# ====================================================================

# Create temporal quality flags

bronze_orders["carrier_before_purchase_flag"] = (bronze_orders["order_delivered_carrier_date"]<bronze_orders["order_purchase_timestamp"])

bronze_orders["delivery_before_carrier_flag"] = (bronze_orders["order_delivered_customer_date"]<bronze_orders["order_delivered_carrier_date"])


# ====================================================================
# Missing timestamp flags
# ====================================================================

# Create missing timestamp flags

bronze_orders["missing_approval_flag"] = (bronze_orders["order_approved_at"].isna())

bronze_orders["missing_carrier_date_flag"] = (bronze_orders["order_delivered_carrier_date"].isna())

bronze_orders["missing_delivery_date_flag"] = (bronze_orders["order_delivered_customer_date"].isna())


# ====================================================================
# Flag validation
# ====================================================================

# Validate temporal quality flags

print("Carrier before purchase:",bronze_orders["carrier_before_purchase_flag"].sum())

print("Delivery before carrier:",bronze_orders["delivery_before_carrier_flag"].sum())

print("Missing approval timestamp:",bronze_orders["missing_approval_flag"].sum())

print("Missing carrier timestamp:",bronze_orders["missing_carrier_date_flag"].sum())

print("Missing customer delivery timestamp:",bronze_orders["missing_delivery_date_flag"].sum())


# ====================================================================
# Quality flag summary
# ====================================================================

# Summary of quality flags

quality_flag_summary = pd.DataFrame({
    "flag": [
        "carrier_before_purchase_flag",
        "delivery_before_carrier_flag",
        "missing_approval_flag",
        "missing_carrier_date_flag",
        "missing_delivery_date_flag"],
    "count": [
        bronze_orders["carrier_before_purchase_flag"].sum(),
        bronze_orders["delivery_before_carrier_flag"].sum(),
        bronze_orders["missing_approval_flag"].sum(),
        bronze_orders["missing_carrier_date_flag"].sum(),
        bronze_orders["missing_delivery_date_flag"].sum()]})

quality_flag_summary["percentage"] = (quality_flag_summary["count"] / len(bronze_orders) * 100).round(3)

display(quality_flag_summary)


# ====================================================================
# 3. Silver Data Validation Orders
# Validate the cleaned orders dataset before creating the Silver layer.
# The Silver layer preserves the original order-level data and includes data-quality flags identified during preprocessing. Business features are intentionally excluded and will be created later in the Gold layer.
# ====================================================================

# Create Silver dataset from validated orders data
silver_orders = bronze_orders.copy()

# Create silver unique key
silver_orders.insert(
    0,
    "id_orders",
    range(1, len(silver_orders) + 1)
)

# Expected Silver schema
expected_silver_columns = [
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


# Validate row count against raw dataset
assert len(silver_orders) == orders_raw_row_count

# Validate silver unique key
assert silver_orders["id_orders"].notna().all()
assert silver_orders["id_orders"].is_unique
assert silver_orders["id_orders"].min() == 1
assert silver_orders["id_orders"].max() == len(silver_orders)


# Validate primary key
assert silver_orders["order_id"].is_unique


# Reorder columns according to the Silver schema
silver_orders = silver_orders[expected_silver_columns]


# Validate expected columns
assert list(silver_orders.columns) == expected_silver_columns


# Validate required key fields
assert silver_orders["order_id"].notna().all()
assert silver_orders["customer_id"].notna().all()
assert silver_orders["order_status"].notna().all()
assert silver_orders["order_purchase_timestamp"].notna().all()


# Validate temporal data types
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

assert all(
    pd.api.types.is_datetime64_any_dtype(silver_orders[column])
    for column in date_columns
)


# Validate quality flag data types
quality_flags = [
    "carrier_before_purchase_flag",
    "delivery_before_carrier_flag",
    "missing_approval_flag",
    "missing_carrier_date_flag",
    "missing_delivery_date_flag"
]

assert all(
    silver_orders[column].dtype == bool
    for column in quality_flags
)


# Validate temporal anomaly flags
assert (
    (
        silver_orders["carrier_before_purchase_flag"]
        != (
            silver_orders["order_delivered_carrier_date"]
            < silver_orders["order_purchase_timestamp"]
        )
    ).sum()
    == 0
)

assert (
    (
        silver_orders["delivery_before_carrier_flag"]
        != (
            silver_orders["order_delivered_customer_date"]
            < silver_orders["order_delivered_carrier_date"]
        )
    ).sum()
    == 0
)


# Validate missing timestamp flags
assert (
    (
        silver_orders["missing_approval_flag"]
        != silver_orders["order_approved_at"].isna()
    ).sum()
    == 0
)

assert (
    (
        silver_orders["missing_carrier_date_flag"]
        != silver_orders["order_delivered_carrier_date"].isna()
    ).sum()
    == 0
)

assert (
    (
        silver_orders["missing_delivery_date_flag"]
        != silver_orders["order_delivered_customer_date"].isna()
    ).sum()
    == 0
)


# Create Silver quality summary
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


# Final Silver validation
assert len(silver_orders) == orders_raw_row_count
assert silver_orders["order_id"].is_unique
assert list(silver_orders.columns) == expected_silver_columns


print("Silver data validation passed.")
print(f"Rows: {len(silver_orders):,}")
print(f"Unique order_ids: {silver_orders['order_id'].nunique():,}")
print(f"Columns: {len(silver_orders.columns)}")
print("Silver schema column order:")
print(list(silver_orders.columns))


# ====================================================================
# 4. Orders – Preprocessing Summary
# The orders dataset was validated and prepared for the Silver layer.
# Data Layers
# The preprocessing follows a simple Bronze-to-Silver architecture.
# - **Bronze:** `bronze_orders` and `bronze_customers` contain the loaded source data.
# - **Silver:** `silver_orders` contains the validated order-level data, including technical and data-quality fields.
# - **Gold:** Business features and analytical KPIs will be created in a separate Gold layer.
# Data quality
# - The `order_id` primary key is unique across all records.
# - Customer references were validated against the customer dataset.
# - Missing timestamps were assessed in the context of order status.
# - Temporal inconsistencies were identified and flagged rather than silently corrected.
# - Original timestamp values were preserved.
# Quality flags
# The following data-quality flags were created:
# - `carrier_before_purchase_flag`
# - `delivery_before_carrier_flag`
# - `missing_approval_flag`
# - `missing_carrier_date_flag`
# - `missing_delivery_date_flag`
# Temporal inconsistencies remain in the original data and are explicitly identified through quality flags.
# Missing timestamp values were retained as `NaN` where no reliable imputation was possible.
# Silver layer
# The resulting Silver dataset preserves the original order-level observations and adds explicit data-quality indicators.
# Business features and analytical KPIs are intentionally not included in the Silver layer. These will be created in the separate Gold layer based on the validated Silver data.
# The Silver dataset is ready for downstream data modeling, feature engineering and business analysis.
# ====================================================================


# ====================================================================
# ORDER REVIEWS – Silver Preprocessing
# ---
# **Dataset:** `olist_order_reviews_dataset.csv`
# **Silver output:** `silver_order_reviews_en.csv`
# This section remains functionally separated from Customers and Orders.
# ====================================================================


# ====================================================================
# 1. Data Understanding
# Inspect the structure, granularity, data types, and basic characteristics of the order reviews dataset before applying any transformations.
# The objective is to understand how reviews are represented in the raw data and identify potential data quality issues that require further investigation.
# ====================================================================


# ====================================================================
# Data Overview
# ====================================================================

bronze_order_reviews.shape

bronze_order_reviews.head()

bronze_order_reviews.info()

bronze_order_reviews.describe(include="all")


# ====================================================================
# Schema & Column Overview
# ====================================================================

bronze_order_reviews.columns.tolist()


expected_columns = [
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

assert bronze_order_reviews.columns.tolist() == expected_columns

bronze_order_reviews.dtypes


# ====================================================================
# Granularity & Relationships
# ====================================================================

#review_id
print("Unique review_id:", bronze_order_reviews["review_id"].nunique())
print("Rows with duplicated review_id:", bronze_order_reviews["review_id"].duplicated().sum())

#order_id
print("Unique order_id:", bronze_order_reviews["order_id"].nunique())
print("Rows with duplicated order_id:", bronze_order_reviews["order_id"].duplicated().sum())

review_order_counts = (
    bronze_order_reviews
    .groupby("review_id")["order_id"]
    .nunique()
    .value_counts()
    .sort_index()
)

review_order_counts

order_review_counts = (
    bronze_order_reviews
    .groupby("order_id")["review_id"]
    .nunique()
    .value_counts()
    .sort_index()
)

order_review_counts


# ====================================================================
# Review Score Distribution
# ====================================================================

bronze_order_reviews["review_score"].value_counts().sort_index()

bronze_order_reviews["review_score"].describe()


# ====================================================================
# Date & Time Characteristics
# ====================================================================

bronze_order_reviews[
    ["review_creation_date", "review_answer_timestamp"]
].dtypes

bronze_order_reviews[
    ["review_creation_date", "review_answer_timestamp"]
].head()

review_creation_dt = pd.to_datetime(
    bronze_order_reviews["review_creation_date"],
    errors="coerce"
)

review_answer_dt = pd.to_datetime(
    bronze_order_reviews["review_answer_timestamp"],
    errors="coerce"
)

print(
    "Review creation:",
    review_creation_dt.min(),
    "to",
    review_creation_dt.max()
)

print(
    "Review answer:",
    review_answer_dt.min(),
    "to",
    review_answer_dt.max()
)


# ====================================================================
# Chapter Summary
# The order reviews dataset contains 99,224 records across seven columns covering review identifiers, order identifiers, review scores, review text, and review timestamps.
# The analysis shows that review IDs and order IDs are not strictly unique. Most review IDs are associated with one order, while a smaller number are associated with multiple orders. Conversely, most orders contain one review record, while a limited number contain multiple review records. Therefore, neither identifier is sufficient to define a unique row across the complete dataset.
# Review scores range from 1 to 5, with higher scores occurring substantially more frequently than lower scores.
# The review creation dates cover the period from October 2016 to August 2018, while review answer timestamps extend from October 2016 to October 2018.
# The raw dataset stores the timestamp fields as strings. Their values follow a consistent datetime representation and will be evaluated further during the data quality assessment and transformation phase.
# Overall, the dataset structure and granularity are sufficiently understood to proceed to a dedicated data quality assessment before applying any transformations.
# ====================================================================


# ====================================================================
# 2. Data Quality Assessment
# Evaluate the data quality of the order reviews dataset before applying transformations.
# The assessment focuses on missing values, duplicate records, valid value ranges, datetime consistency, and text field quality. The objective is to identify issues that require treatment during preprocessing while preserving valid characteristics of the raw dataset.
# ====================================================================


# ====================================================================
# Missing Value Assessment
# ====================================================================

missing_summary = (
    bronze_order_reviews.isna()
    .sum()
    .to_frame("missing_count")
)

missing_summary["missing_pct"] = (
    missing_summary["missing_count"]
    / len(bronze_order_reviews)
    * 100
)

missing_summary

mandatory_columns = [
    "review_id",
    "order_id",
    "review_score",
    "review_creation_date",
    "review_answer_timestamp"
]

bronze_order_reviews[mandatory_columns].isna().sum()

assert bronze_order_reviews[mandatory_columns].notna().all().all()

comment_columns = [
    "review_comment_title",
    "review_comment_title_en",
    "review_comment_message",
    "review_comment_message_en"
]

bronze_order_reviews[comment_columns].isna().sum()

empty_text_summary = {}

for column in comment_columns:
    empty_text_summary[column] = {
        "empty_string": (bronze_order_reviews[column] == "").sum(),
        "whitespace_only":bronze_order_reviews[column].str.strip().eq("").sum()
    }

empty_text_summary


# ====================================================================
# Duplicate Record Validation
# ====================================================================

exact_duplicates = bronze_order_reviews.duplicated().sum()

exact_duplicates

review_id_duplicate_rows = bronze_order_reviews["review_id"].duplicated().sum()

review_id_duplicate_rows

order_id_duplicate_rows = bronze_order_reviews["order_id"].duplicated().sum()

order_id_duplicate_rows


# ====================================================================
# Value Validation
# ====================================================================

bronze_order_reviews["review_score"].value_counts().sort_index()

assert bronze_order_reviews["review_score"].between(1, 5).all() #kapitel3


# ====================================================================
# Datetime validation
# ====================================================================

review_creation_dt = pd.to_datetime(
    bronze_order_reviews["review_creation_date"],
    errors="coerce"
)

review_answer_dt = pd.to_datetime(
    bronze_order_reviews["review_answer_timestamp"],
    errors="coerce"
)

print("Invalid review_creation_date:", review_creation_dt.isna().sum())
print("Invalid review_answer_timestamp:", review_answer_dt.isna().sum())

assert review_creation_dt.notna().all()
assert review_answer_dt.notna().all()

answer_before_creation = review_answer_dt < review_creation_dt

answer_before_creation.sum()

assert not answer_before_creation.any()


# ====================================================================
# Text Field Validation
# ====================================================================

blank_text_summary = {}

for column in comment_columns:
    blank_text_summary[column] = (
        bronze_order_reviews[column].notna()
        & bronze_order_reviews[column].str.strip().eq("")
    ).sum()

blank_text_summary


# ====================================================================
# Chapter Summary
# The data quality assessment identified no missing values in mandatory identifiers, review scores, or timestamp fields.
# The review comment fields contain substantial missingness, which is treated as expected because review text is optional. A small number of non-null comment values contain only whitespace and will be normalized during preprocessing.
# No exact duplicate rows were identified. Repeated `review_id` and `order_id` values do not represent exact duplicate records and therefore do not require record removal.
# All review scores are within the valid range of 1 to 5.
# Both timestamp fields can be successfully parsed as datetime values, and no chronological inconsistencies were identified between review creation and answer timestamps.
# Overall, no critical data quality issues requiring record-level removal were identified. The main preprocessing requirements are the normalization of text fields and conversion of timestamp fields to appropriate datetime types.
# ====================================================================


# ====================================================================
# 3. Data Transformation
# Apply the required transformations identified during the data quality assessment to create a clean Silver version of the order reviews dataset.
# The transformations focus on text normalization and datetime conversion while preserving the original review content and row-level structure of the dataset.
# ====================================================================


# ====================================================================
# Create Silver Dataset
# ====================================================================

silver_order_reviews = bronze_order_reviews.copy()

silver_order_reviews.shape

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
assert silver_order_reviews["id_order_reviews"].max() == len(silver_order_reviews)


# ====================================================================
# Text Normalization
# ====================================================================

comment_columns = [
    "review_comment_title",
    "review_comment_message"
]

for column in comment_columns:
    silver_order_reviews[column] = (
        silver_order_reviews[column]
        .astype("string")
        .str.lower()
        .str.replace(r"[^a-z\s.,!?]", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
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
        .str.replace(r"[^a-z\s.,!?]", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .replace("", pd.NA)
    )

silver_order_reviews.loc[
    silver_order_reviews["review_comment_title"] == "nota dez",
    "review_comment_title_en"
] = "ranking ten"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_title"] == "nota",
    "review_comment_title_en"
] = "ranking"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_message"] == "nota",
    "review_comment_message_en"
] = "ranking"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_title"] == "nenhuma",
    "review_comment_title_en"
] = "none"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_message"] == "nenhuma",
    "review_comment_message_en"
] = "none"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_message"] == "nd",
    "review_comment_message_en"
] = "not available"

silver_order_reviews.loc[
    silver_order_reviews["review_comment_message"] == "no h",
    "review_comment_message_en"
] = "there is no"

for column in comment_columns + translation_columns:
    non_null_values = silver_order_reviews[column].dropna()

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

silver_order_reviews[
    [
        "review_comment_title",
        "review_comment_title_en",
        "review_comment_message",
        "review_comment_message_en"
    ]
].head(10)


# ====================================================================
# Datetime Transformation
# ====================================================================

datetime_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in datetime_columns:
    silver_order_reviews[column] = pd.to_datetime(
        silver_order_reviews[column],
        errors="raise"
    )

silver_order_reviews[datetime_columns].dtypes

assert silver_order_reviews[datetime_columns].notna().all().all()

answer_before_creation = (
    silver_order_reviews["review_answer_timestamp"]
    < silver_order_reviews["review_creation_date"]
)

assert not answer_before_creation.any()


# ====================================================================
# Transformation Validation
# ====================================================================

silver_order_reviews.info()

assert len(silver_order_reviews) == len(bronze_order_reviews)
assert silver_order_reviews["review_id"].nunique() == bronze_order_reviews["review_id"].nunique()
assert silver_order_reviews["order_id"].nunique() == bronze_order_reviews["order_id"].nunique()


# ====================================================================
# Silver Dataset Overview
# ====================================================================

silver_order_reviews.head()

silver_order_reviews.dtypes


# ====================================================================
# Order Reviews Dataset Summary
# The order reviews dataset was transformed into a clean Silver version while preserving the original row-level structure and review identifiers.
# The Silver dataset receives a unique key `id_order_reviews` to uniquely identify each review record. The key starts at 1 and preserves the row-level grain of the dataset. The existing `review_id` and `order_id` fields are retained as business identifiers and relationship keys.
# The Portuguese review text fields were normalized by converting text to lowercase, removing leading and trailing whitespace, standardizing whitespace, and removing characters outside the defined character set. Empty text values were converted to missing values. The original Portuguese review content was retained.
# The English review title and message fields were normalized using the same text transformation rules. Missing English translations for specific rating-related values were completed using defined mappings, while the Portuguese original values remained unchanged. This ensured consistency between the original and translated review fields.
# The review creation date and answer timestamp were converted from strings to datetime values. The resulting timestamps remain complete and chronologically consistent.
# No records were removed and no identifier values were altered during the transformation.
# The resulting Silver dataset preserves the original review information while providing standardized Portuguese and English text fields and appropriately typed timestamp columns. It is now prepared for downstream analysis and integration with the other Olist datasets.
# ====================================================================


# ====================================================================
# 5. Final Silver Validation & Common Export
# All three Silver datasets are finally validated after their respective transformations.
# The export is performed **only once at the end** for all three datasets.
# ====================================================================

# ============================================================
# Final validation – Customers
# ============================================================

expected_customers_columns = [
    "id_customers",
    "customer_id",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state"
]

assert silver_customers.columns.tolist() == expected_customers_columns
assert len(silver_customers) == customers_raw_row_count

assert silver_customers["id_customers"].notna().all()
assert silver_customers["id_customers"].is_unique
assert silver_customers["id_customers"].min() == 1
assert silver_customers["id_customers"].max() == len(silver_customers)

assert silver_customers["customer_id"].notna().all()
assert silver_customers["customer_id"].is_unique
assert silver_customers["customer_unique_id"].notna().all()
assert silver_customers["customer_city"].notna().all()
assert silver_customers["customer_state"].notna().all()
assert silver_customers.isna().sum().sum() == 0

assert invalid_states == set()

assert silver_customers["customer_zip_code_prefix"].str.len().eq(5).all()
assert silver_customers["customer_zip_code_prefix"].str.isnumeric().all()

print("Customers Silver validation passed.")

# ============================================================
# Final validation – Orders
# ============================================================

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

assert silver_orders.columns.tolist() == expected_orders_columns
assert len(silver_orders) == orders_raw_row_count

assert silver_orders["id_orders"].notna().all()
assert silver_orders["id_orders"].is_unique
assert silver_orders["id_orders"].min() == 1
assert silver_orders["id_orders"].max() == len(silver_orders)

assert silver_orders["order_id"].notna().all()
assert silver_orders["order_id"].is_unique
assert silver_orders["customer_id"].notna().all()
assert silver_orders["order_status"].notna().all()
assert silver_orders["order_purchase_timestamp"].notna().all()

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

assert all(
    pd.api.types.is_datetime64_any_dtype(silver_orders[column])
    for column in date_columns
)

quality_flags = [
    "carrier_before_purchase_flag",
    "delivery_before_carrier_flag",
    "missing_approval_flag",
    "missing_carrier_date_flag",
    "missing_delivery_date_flag"
]

assert all(
    silver_orders[column].dtype == bool
    for column in quality_flags
)

print("Orders Silver validation passed.")

# ============================================================
# Final validation – Order Reviews
# ============================================================

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

assert silver_order_reviews.columns.tolist() == expected_order_reviews_columns
assert len(silver_order_reviews) == order_reviews_raw_row_count

assert silver_order_reviews["id_order_reviews"].notna().all()
assert silver_order_reviews["id_order_reviews"].is_unique
assert silver_order_reviews["id_order_reviews"].min() == 1
assert silver_order_reviews["id_order_reviews"].max() == len(silver_order_reviews)

mandatory_columns = [
    "review_id",
    "order_id",
    "review_score",
    "review_creation_date",
    "review_answer_timestamp"
]

assert silver_order_reviews[mandatory_columns].notna().all().all()
assert silver_order_reviews["review_score"].between(1, 5).all()

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

print("Order Reviews Silver validation passed.")


# ====================================================================
# 5.1 Common Silver Export
# ====================================================================

# Export all validated Silver datasets once

# customers_output = PROCESSED_PATH / "silver_customers.csv"
# orders_output = PROCESSED_PATH / "silver_orders.csv"
# order_reviews_output = PROCESSED_PATH / "silver_order_reviews_en.csv"

# silver_customers.to_csv(
#    customers_output,
#    index=False
# )

# silver_orders.to_csv(
#    orders_output,
#    index=False
# )

# silver_order_reviews.to_csv(
#   order_reviews_output,
#   index=False
# )

# print("Silver datasets exported successfully:")
# print(f"- Customers:     {customers_output}")
# print(f"- Orders:        {orders_output}")
# print(f"- Order Reviews: {order_reviews_output}")


# ====================================================================
# S3 SILVER EXPORT – FUTURE AWS LAMBDA VERSION
# This block is intentionally commented out.
# It will be activated when the preprocessing pipeline is moved from local processing to AWS Lambda.
# All three validated Silver datasets are uploaded to:
# s3://dsi-final-project-360964564955-eu-central-1-an/processed/
# ====================================================================


# import boto3
# from io import StringIO


# ------------------------------------------------------------
# S3 Configuration
# ------------------------------------------------------------

# S3_BUCKET = "dsi-final-project-360964564955-eu-central-1-an"
# PROCESSED_PREFIX = "processed/"


# ------------------------------------------------------------
# S3 Client
# ------------------------------------------------------------

# s3 = boto3.client("s3")


# ------------------------------------------------------------
# Helper function: Upload DataFrame to S3 as CSV
# ------------------------------------------------------------

# def save_csv_to_s3(df, bucket, key):
#
#     csv_buffer = StringIO()
#
#     df.to_csv(
#         csv_buffer,
#         index=False
#     )
#
#     s3.put_object(
#         Bucket=bucket,
#         Key=key,
#         Body=csv_buffer.getvalue(),
#         ContentType="text/csv"
#     )
#
#     print(f"Successfully uploaded: s3://{bucket}/{key}")


# ------------------------------------------------------------
# Export Silver datasets to S3
# ------------------------------------------------------------

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


# print("All Silver datasets successfully exported to S3.")


# ====================================================================
# 6. Combined Silver Layer Summary
# This notebook combines the three existing preprocessing pipelines into one common execution:
# - **Customers:** Standardization of IDs, City, State and ZIP Prefix, including `id_customers`.
# - **Orders:** Validation of Order/Customer relationships, datetime conversion, temporal quality flags and `id_orders`.
# - **Order Reviews:** Text normalization, defined translation adjustments, datetime conversion and `id_order_reviews`.
# The three datasets remain clearly separated within the notebook. The shared setup and common export are executed only once.
# ====================================================================

