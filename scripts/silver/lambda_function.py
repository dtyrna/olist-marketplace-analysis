import boto3
from io import BytesIO, StringIO

import numpy as np
import pandas as pd
from unidecode import unidecode


S3_BUCKET = "dsi-final-project-360964564955-eu-central-1-an"
SOURCE_PREFIX = "_raw/"
TARGET_PREFIX = "test/"


SOURCE_FILES = {
    "customers": "_raw/olist_customers_dataset.csv",
    "geolocation": "_raw/olist_geolocation_dataset.csv",
    "order_items": "_raw/olist_order_items_dataset.csv",
    "order_payments": "_raw/olist_order_payments_dataset.csv",
    "order_reviews": "_raw/olist_order_reviews_dataset_en.csv",
    "orders": "_raw/olist_orders_dataset.csv",
    "products": "_raw/olist_products_dataset.csv",
    "sellers": "_raw/olist_sellers_dataset.csv",
    "category_translation": (
        "_raw/product_category_name_translation.csv"
    ),
}


TARGET_FILES = {
    "customers": "test/customers/silver_customers.csv",
    "geolocation": "test/geolocation/silver_geolocation.csv",
    "order_items": "test/order_items/silver_order_items.csv",
    "order_payments": (
        "test/order_payments/silver_order_payments.csv"
    ),
    "order_reviews": (
        "test/order_reviews/silver_order_reviews_en.csv"
    ),
    "orders": "test/orders/silver_orders.csv",
    "products": "test/products/silver_products.csv",
    "sellers": "test/sellers/silver_sellers.csv",
    "category_translation": (
        "test/category_translation/silver_category_translation.csv"
    ),
}


s3 = boto3.client("s3")


def load_csv_from_s3(bucket, key):
    """
    Load a CSV file from S3 into a pandas DataFrame.
    """
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(
            BytesIO(response["Body"].read()),
            encoding="utf-8",
        )
    except Exception as error:
        raise RuntimeError(
            f"Failed to load source file s3://{bucket}/{key}: "
            f"{error}"
        ) from error


def load_source_data():
    """
    Load all predefined source files from S3.
    """
    return {
        name: load_csv_from_s3(S3_BUCKET, key)
        for name, key in SOURCE_FILES.items()
    }


def save_csv_to_s3(dataframe, bucket, key):
    """
    Upload a pandas DataFrame to S3 as a UTF-8 CSV file.
    """
    try:
        csv_buffer = StringIO()
        dataframe.to_csv(
            csv_buffer,
            index=False,
            encoding="utf-8",
        )
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=csv_buffer.getvalue().encode("utf-8"),
            ContentType="text/csv; charset=utf-8",
        )
        print(f"Successfully uploaded s3://{bucket}/{key}")
    except Exception as error:
        raise RuntimeError(
            f"Failed to save target file s3://{bucket}/{key}: {error}"
        ) from error


def transform_order_payments(bronze_order_payments):
    """Transform the order payments source DataFrame."""
    try:
        df = bronze_order_payments.copy()
        numeric_columns = [
            "payment_sequential",
            "payment_installments",
            "payment_value",
        ]
        string_columns = ["order_id", "payment_type"]

        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors="raise")
        for column in string_columns:
            df[column] = df[column].astype("str")

        df = df[df["payment_type"] != "not_defined"]
        df = df[df["payment_value"] != 0]
        df = df.dropna(
                        subset=["payment_value"]
                    )
        df["id_order_payments"] = np.arange(1, len(df) + 1)
        return df[df.columns.sort_values()]
    except Exception as error:
        raise RuntimeError(
            f"Order payments transformation failed: {error}"
        ) from error


def transform_products(bronze_products):
    """Transform the products source DataFrame."""
    try:
        df = bronze_products.copy()
        numeric_columns = [
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ]
        string_columns = ["product_id", "product_category_name"]

        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors="raise")
        for column in string_columns:
            df[column] = df[column].astype("str")

        product_id_is_unique = (
            df.dropna(subset="product_id").shape[0] == len(df)
            and df["product_id"].nunique() == len(df)
        )
        if not product_id_is_unique:
            if df.dropna(subset="product_id").shape[0] < len(df):
                product_id_is_unique = False
            else:
                raise ValueError("Duplicate product_id values were found.")

        data_columns = df.columns.drop("product_id")
        df = df.dropna(subset=data_columns, how="all")

        if product_id_is_unique:
            df["id_products"] = np.arange(1, len(df) + 1)
        return df[df.columns.sort_values()]
    except Exception as error:
        raise RuntimeError(
            f"Products transformation failed: {error}"
        ) from error


def transform_sellers(bronze_sellers):
    """Transform the sellers source DataFrame."""
    try:
        df = bronze_sellers.copy()
        string_columns = [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state",
        ]
        for column in string_columns:
            df[column] = df[column].astype("str")

        seller_id_is_unique = (
            df.dropna(subset="seller_id").shape[0] == len(df)
            and df["seller_id"].nunique() == len(df)
        )
        if not seller_id_is_unique:
            if df.dropna(subset="seller_id").shape[0] >= len(df):
                raise ValueError("Duplicate seller_id values were found.")

        data_columns = df.columns.drop("seller_id")
        df = df.dropna(subset=data_columns, how="all")

        city_mask = (
            df["seller_city"].str.lower().apply(unidecode)
            != df["seller_city"]
        )
        df.loc[city_mask, "seller_city"] = (
            df.loc[city_mask, "seller_city"].apply(unidecode)
        )

        for character in [",", ";", "/"]:
            df["seller_city"] = (
                df["seller_city"]
                .str.split(character)
                .str[0]
                .str.strip()
            )

        df["seller_city"] = df["seller_city"].astype("str")
        for state in sorted(df["seller_state"].unique()):
            if state != state.lower().strip() or len(state) != 2:
                corrected_state = state.lower().strip()[:2]
                df["seller_state"] = df["seller_state"].str.replace(
                    state,
                    corrected_state,
                )

        if seller_id_is_unique:
            df["id_sellers"] = np.arange(1, len(df) + 1)
        return df[df.columns.sort_values()]
    except Exception as error:
        raise RuntimeError(
            f"Sellers transformation failed: {error}"
        ) from error


def transform_customers(bronze_customers):
    """Transform and validate the customers source DataFrame."""
    try:
        raw_row_count = len(bronze_customers)
        df = bronze_customers.copy()
        df.insert(0, "id_customers", range(1, len(df) + 1))

        string_columns = [
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "customer_state",
        ]
        for column in string_columns:
            df[column] = df[column].str.strip()

        df["customer_state"] = df["customer_state"].str.lower()
        df["customer_city"] = (
            df["customer_city"]
            .str.lower()
            .str.replace("-", " ", regex=False)
            .str.replace("'", "", regex=False)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )
        df.loc[
            df["customer_city"] == "quilometro 14 do mutum",
            "customer_city",
        ] = "mutum"

        for column in string_columns:
            df[column] = df[column].astype("string")
        df["customer_zip_code_prefix"] = (
            df["customer_zip_code_prefix"].astype("string").str.zfill(5)
        )

        valid_states = {
            "sp", "sc", "mg", "pr", "rj", "rs", "pa", "go", "es",
            "ba", "ma", "ms", "ce", "df", "rn", "pe", "mt", "am",
            "ap", "al", "ro", "pb", "to", "pi", "ac", "se", "rr",
        }
        invalid_states = set(df["customer_state"].dropna().unique()) - valid_states

        assert df["customer_id"].notna().all()
        assert df["customer_id"].is_unique
        assert df["customer_unique_id"].notna().all()
        assert df["customer_zip_code_prefix"].str.len().eq(5).all()
        assert df["customer_zip_code_prefix"].str.isnumeric().all()
        assert len(df) == raw_row_count
        assert df["id_customers"].is_unique
        assert df["customer_city"].str.match(r"^[a-z\s]+$").all()
        assert df["customer_state"].notna().all()
        assert df.isna().sum().sum() == 0
        assert invalid_states == set()
        return df
    except Exception as error:
        raise RuntimeError(
            f"Customers transformation failed: {error}"
        ) from error


def transform_orders(bronze_orders, silver_customers):
    """Transform and validate the orders source DataFrame."""
    try:
        raw_row_count = len(bronze_orders)
        df = bronze_orders.copy()
        date_columns = [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
        df[date_columns] = df[date_columns].apply(pd.to_datetime)
        df["carrier_before_purchase_flag"] = (
            df["order_delivered_carrier_date"]
            < df["order_purchase_timestamp"]
        )
        df["delivery_before_carrier_flag"] = (
            df["order_delivered_customer_date"]
            < df["order_delivered_carrier_date"]
        )
        df["missing_approval_flag"] = df["order_approved_at"].isna()
        df["missing_carrier_date_flag"] = (
            df["order_delivered_carrier_date"].isna()
        )
        df["missing_delivery_date_flag"] = (
            df["order_delivered_customer_date"].isna()
        )
        quality_flags = [
            "carrier_before_purchase_flag",
            "delivery_before_carrier_flag",
            "missing_approval_flag",
            "missing_carrier_date_flag",
            "missing_delivery_date_flag",
        ]
        mapping = silver_customers[["customer_id", "customer_unique_id"]].copy()
        assert mapping["customer_id"].is_unique
        df = df.merge(mapping, on="customer_id", how="left", validate="many_to_one")
        assert len(df) == raw_row_count
        assert df["customer_unique_id"].notna().all()
        df.insert(0, "id_orders", range(1, len(df) + 1))
        expected_columns = [
            "id_orders", "order_id", "customer_id", "customer_unique_id",
            "order_status", "order_purchase_timestamp", "order_approved_at",
            "order_delivered_carrier_date", "order_delivered_customer_date",
            "order_estimated_delivery_date", *quality_flags,
        ]
        df = df[expected_columns]
        assert df.columns.tolist() == expected_columns
        assert len(df) == raw_row_count
        assert df["id_orders"].is_unique
        assert df["order_id"].notna().all()
        assert df["order_id"].is_unique
        assert df["customer_id"].notna().all()
        assert df["customer_unique_id"].notna().all()
        assert df["order_status"].notna().all()
        assert df["order_purchase_timestamp"].notna().all()
        assert all(pd.api.types.is_datetime64_any_dtype(df[column]) for column in date_columns)
        assert all(df[column].dtype == bool for column in quality_flags)
        return df
    except Exception as error:
        raise RuntimeError(
            f"Orders transformation failed: {error}"
        ) from error


def transform_order_reviews(bronze_order_reviews):
    """Transform and validate the order reviews source DataFrame."""
    try:
        raw_row_count = len(bronze_order_reviews)
        df = bronze_order_reviews.copy()
        expected_input_columns = [
            "review_id", "order_id", "review_score",
            "review_comment_title", "review_comment_title_en",
            "review_comment_message", "review_comment_message_en",
            "review_creation_date", "review_answer_timestamp",
        ]
        assert df.columns.tolist() == expected_input_columns
        mandatory_columns = [
            "review_id", "order_id", "review_score",
            "review_creation_date", "review_answer_timestamp",
        ]
        assert df[mandatory_columns].notna().all().all()
        assert df["review_score"].between(1, 5).all()
        creation = pd.to_datetime(df["review_creation_date"], errors="coerce")
        answer = pd.to_datetime(df["review_answer_timestamp"], errors="coerce")
        assert creation.notna().all()
        assert answer.notna().all()
        assert not (answer < creation).any()
        df["id_order_reviews"] = range(1, len(df) + 1)
        df.insert(0, "id_order_reviews", df.pop("id_order_reviews"))
        comment_columns = ["review_comment_title", "review_comment_message"]
        translation_columns = [
            "review_comment_title_en", "review_comment_message_en",
        ]
        for column in comment_columns + translation_columns:
            df[column] = (
                df[column].astype("string").str.lower()
                .str.replace(r"[^a-z\s.,!?]", "", regex=True)
                .str.replace(r"\s+", " ", regex=True)
                .str.strip().replace("", pd.NA)
            )
        mappings = [
            ("review_comment_title", "nota dez", "review_comment_title_en", "ranking ten"),
            ("review_comment_title", "nota", "review_comment_title_en", "ranking"),
            ("review_comment_message", "nota", "review_comment_message_en", "ranking"),
            ("review_comment_title", "nenhuma", "review_comment_title_en", "none"),
            ("review_comment_message", "nenhuma", "review_comment_message_en", "none"),
            ("review_comment_message", "nd", "review_comment_message_en", "not available"),
            ("review_comment_message", "no h", "review_comment_message_en", "there is no"),
        ]
        for source_column, source_value, target_column, target_value in mappings:
            df.loc[df[source_column] == source_value, target_column] = target_value
        for column in comment_columns + translation_columns:
            values = df[column].dropna()
            assert (values == values.str.strip()).all()
            assert (values == values.str.lower()).all()
            assert values.str.match(r"^[a-z\s.,!?]+$").all()
        assert (df["review_comment_title"].isna() == df["review_comment_title_en"].isna()).all()
        assert (df["review_comment_message"].isna() == df["review_comment_message_en"].isna()).all()
        for column in ["review_creation_date", "review_answer_timestamp"]:
            df[column] = pd.to_datetime(df[column], errors="raise")
        assert not (df["review_answer_timestamp"] < df["review_creation_date"]).any()
        expected_columns = [
            "id_order_reviews", "review_id", "order_id", "review_score",
            "review_comment_title", "review_comment_title_en",
            "review_comment_message", "review_comment_message_en",
            "review_creation_date", "review_answer_timestamp",
        ]
        df = df[expected_columns]
        assert len(df) == raw_row_count
        assert df["id_order_reviews"].is_unique
        assert df["review_score"].between(1, 5).all()
        return df
    except Exception as error:
        raise RuntimeError(
            f"Order reviews transformation failed: {error}"
        ) from error


def transform_geolocation(bronze_geolocation):
    """Transform the geolocation source DataFrame."""
    try:
        df = bronze_geolocation.copy()
        df[["geolocation_city", "geolocation_state"]] = df[
            ["geolocation_city", "geolocation_state"]
        ].astype("string")
        df = df.drop_duplicates(
            subset=["geolocation_zip_code_prefix"],
            keep="first",
        )
        df["geolocation_state"] = df["geolocation_state"].str.strip().str.lower()
        replacements = {
            "â": "a", "í": "i", "ó": "o", "ô": "o", "õ": "o",
            "ü": "u", "´": "", "`": "", "º": "",
        }
        df["geolocation_city"] = (
            df["geolocation_city"].str.lower().str.strip()
            .replace(replacements, regex=True)
            .str.replace(r"[^a-z\s\-]", "", regex=True)
            .str.strip()
        )
        orthography = {
            "so paulo": "sao paulo", "jos bonifcio": "jose bonifacio",
            "jose bonifactio": "jose bonifacio", "sopaulo": "sao paulo",
            "sp": "sao paulo", "poa": "porto alegre", "po": "port alegre",
            "mogidascruzes": "mogi das cruzes", "biritiba-mirim": "biritiba mirim",
            "santo andr": "santo andre",
        }
        df["geolocation_city"] = df["geolocation_city"].replace(orthography, regex=True)
        combinations = (
            df.groupby(["geolocation_city", "geolocation_state"])
            .size()
            .reset_index(name="count")
            .sort_values(["geolocation_city", "count"], ascending=[True, False])
            .drop_duplicates(subset=["geolocation_city"])
        )
        mapping = dict(zip(combinations["geolocation_city"], combinations["geolocation_state"]))
        df["geolocation_state"] = df["geolocation_city"].map(mapping).astype("string")
        df = df.drop_duplicates()
        df["geolocation_zip_code_prefix"] = (
            df["geolocation_zip_code_prefix"].astype(str).str.zfill(5).astype("string")
        )
        valid_cities = df["geolocation_city"].value_counts()
        df = df[df["geolocation_city"].isin(valid_cities[valid_cities >= 2].index)]
        df = df.reset_index(drop=True)

        df["id_geolocation"] = (
            df.index + 1
        )

        reorder_columns = [
            "id_geolocation",
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng",
            "geolocation_city",
            "geolocation_state",
        ]

        df = df[reorder_columns]

        return df

    except Exception as error:
        raise RuntimeError(
            f"Geolocation transformation failed: {error}"
        ) from error


def transform_category_translation(bronze_category_translation):
    """Transform the category translation source DataFrame."""
    try:
        df = bronze_category_translation.copy()
        columns = [
            "product_category_name",
            "product_category_name_english",
        ]
        df = df[columns].astype("string")
        for column in columns:
            df[column] = df[column].str.strip().str.lower()
        df = df.drop_duplicates().reset_index(drop=True)
        df["id_product_name_translation"] = df.index + 1
        df = df.set_index("id_product_name_translation")
        max_length_portuguese = df["product_category_name"].str.len().max()
        max_length_english = df["product_category_name_english"].str.len().max()
        print(f"Maximum Portuguese category length: {max_length_portuguese}")
        print(f"Maximum English category length: {max_length_english}")
        return df
    except Exception as error:
        raise RuntimeError(
            f"Category translation transformation failed: {error}"
        ) from error

def transform_order_items(bronze_order_items):
    """
    Transform and validate the order items source DataFrame.
    """
    try:
        print("=" * 60)
        print("ORDER ITEMS - SILVER PREPROCESSING")
        print("=" * 60)

        df_order_items = bronze_order_items.copy()

        print("Shape:", df_order_items.shape)
        print("\nColumns:")
        print(df_order_items.columns.tolist())

        print("\nData types:")
        print(df_order_items.dtypes)

        check_order = (
            df_order_items["order_id"]
            .apply(type)
            .value_counts()
        )

        check_product = (
            df_order_items["product_id"]
            .apply(type)
            .value_counts()
        )

        check_seller = (
            df_order_items["seller_id"]
            .apply(type)
            .value_counts()
        )

        check_date = (
            df_order_items["shipping_limit_date"]
            .apply(type)
            .value_counts()
        )

        print("shipping_limit_date types:")
        print(check_date)

        print("order_id types:")
        print(check_order)

        print("product_id types:")
        print(check_product)

        print("seller_id types:")
        print(check_seller)

        df_order_items[
            "shipping_limit_date"
        ] = pd.to_datetime(
            df_order_items[
                "shipping_limit_date"
            ],
            errors="raise",
        )

        df_order_items["seller_id"] = (
            df_order_items["seller_id"]
            .astype("string")
        )

        df_order_items["order_id"] = (
            df_order_items["order_id"]
            .astype("string")
        )

        df_order_items["product_id"] = (
            df_order_items["product_id"]
            .astype("string")
        )

        df_order_items.info()

        null_order_item_id_count = (
            df_order_items[
                "order_item_id"
            ].isna().sum()
        )

        print(
            "Null values in order_item_id:",
            null_order_item_id_count,
        )

        null_price_count = (
            df_order_items[
                "price"
            ].isna().sum()
        )

        print(
            "Null values in price:",
            null_price_count,
        )

        null_freight_value_count = (
            df_order_items[
                "freight_value"
            ].isna().sum()
        )

        print(
            "Null values in freight_value:",
            null_freight_value_count,
        )

        df_order_items["order_id"] = (
            df_order_items["order_id"]
            .str.strip()
            .str.lower()
        )

        df_order_items["product_id"] = (
            df_order_items["product_id"]
            .str.strip()
            .str.lower()
        )

        df_order_items["seller_id"] = (
            df_order_items["seller_id"]
            .str.strip()
            .str.lower()
        )

        order_id_characters = "".join(
            df_order_items["order_id"]
            .dropna()
            .astype(str)
        )

        print(
            "Characters in order_id:",
            sorted(set(order_id_characters)),
        )

        product_id_characters = "".join(
            df_order_items["product_id"]
            .dropna()
            .astype(str)
        )

        print(
            "Characters in product_id:",
            sorted(set(product_id_characters)),
        )

        seller_id_characters = "".join(
            df_order_items["seller_id"]
            .dropna()
            .astype(str)
        )

        print(
            "Characters in seller_id:",
            sorted(set(seller_id_characters)),
        )

        minimum_quantity = (
            df_order_items[
                "order_item_id"
            ].min()
        )

        maximum_quantity = (
            df_order_items[
                "order_item_id"
            ].max()
        )

        print(
            "Order quantity minimum:",
            minimum_quantity,
            "and maximum:",
            maximum_quantity,
        )

        minimum_freight = (
            df_order_items[
                "freight_value"
            ].min()
        )

        maximum_freight = (
            df_order_items[
                "freight_value"
            ].max()
        )

        print(
            "Shipping cost minimum:",
            minimum_freight,
            "and maximum:",
            maximum_freight,
        )

        wrong_floats_freight = (
            (
                df_order_items["price"] * 100
            )
            % 1
            != 0
        ).sum()

        print(
            "Prices with more than two decimal "
            "places before rounding:",
            wrong_floats_freight,
            "rows",
        )

        freight_as_string = (
            df_order_items["price"]
            .round(2)
            .astype(str)
        )

        freight_check = (
            freight_as_string
            .str.split(".")
            .str[1]
            .str.len()
        )

        print(
            "Maximum number of decimal places:",
            freight_check.max(),
        )

        minimum_price = (
            df_order_items["price"].min()
        )

        maximum_price = (
            df_order_items["price"].max()
        )

        print(
            "Order value minimum:",
            minimum_price,
            "and maximum:",
            maximum_price,
        )

        wrong_floats = (
            (
                df_order_items["price"] * 100
            )
            % 1
            != 0
        ).sum()

        print(
            "Prices with more than two decimal "
            "places before rounding:",
            wrong_floats,
            "rows",
        )

        df_order_items["price"] = (
            df_order_items["price"]
            .round(2)
        )

        float_check = (
            (
                df_order_items["price"] * 100
            )
            % 1
            != 0
        ).sum()

        print(
            "Prices with more than two decimal "
            "places after rounding:",
            float_check,
            "rows",
        )

        price_as_string = (
            df_order_items["price"]
            .round(2)
            .astype(str)
        )

        float_check = (
            price_as_string
            .str.split(".")
            .str[1]
            .str.len()
        )

        print(
            "Maximum number of decimal places "
            "after rounding:",
            float_check.max(),
        )

        order_id_lengths = (
            df_order_items["order_id"]
            .str.len()
            .value_counts()
        )

        product_id_lengths = (
            df_order_items["product_id"]
            .str.len()
            .value_counts()
        )

        seller_id_lengths = (
            df_order_items["seller_id"]
            .str.len()
            .value_counts()
        )

        print(
            "Order ID lengths:",
            order_id_lengths,
        )

        print(
            "Product ID lengths:",
            product_id_lengths,
        )

        print(
            "Seller ID lengths:",
            seller_id_lengths,
        )

        df_order_items = (
            df_order_items.reset_index(
                drop=True
            )
        )

        df_order_items = (
                    df_order_items.reset_index(drop=True)
                )
        
        df_order_items["id_olist_order_items"] = (
            df_order_items.index + 1
        )

        duplicate_count = (
            df_order_items.duplicated().sum()
        )

        print(
            "Duplicate rows after surrogate key "
            "creation:",
            duplicate_count,
        )

        print(
            "Order items descriptive statistics:"
        )

        print(df_order_items.describe())

        reorder_columns = [
            "id_olist_order_items",
            "order_id",
            "product_id",
            "seller_id",
            "shipping_limit_date",
            "order_item_id",
            "price",
            "freight_value",
        ]

        df_order_items = df_order_items[
            reorder_columns
        ]

        print(
            "Order items transformation completed "
            "successfully."
        )

        print(
            "Output shape:",
            df_order_items.shape,
        )

        return df_order_items

    except Exception as error:
        raise RuntimeError(
            "Order items transformation failed: "
            f"{error}"
        ) from error

def validate_core_silver_datasets(
    silver_customers,
    silver_orders,
    silver_order_reviews,
    customers_raw_row_count,
    orders_raw_row_count,
    order_reviews_raw_row_count,
):
    """Validate the core Silver datasets."""
    try:
        print("\n" + "=" * 60)
        print("FINAL SILVER VALIDATION")
        print("=" * 60)
        assert len(silver_customers) == customers_raw_row_count
        assert len(silver_orders) == orders_raw_row_count
        assert len(silver_order_reviews) == order_reviews_raw_row_count
        assert silver_customers["customer_id"].is_unique
        assert silver_orders["order_id"].is_unique
        assert silver_order_reviews["id_order_reviews"].is_unique
        assert silver_orders["customer_unique_id"].notna().all()
        print("All three Silver datasets passed the final cross-dataset validation.")
    except Exception as error:
        raise RuntimeError(
            f"Final Silver validation failed: {error}"
        ) from error


def lambda_handler(event, context):
    """Run the complete manual S3-to-S3 transformation workflow."""
    try:
        print("Lambda transformation started.")
        source_data = load_source_data()

        print("Transforming customers...")
        
        silver_customers = transform_customers(source_data["customers"])
        
        print("Customers transformation completed.")

        print("Transforming orders...")

        silver_orders = transform_orders(
            source_data["orders"],
            silver_customers,
        )

        print("Orders transformation completed.")
  
        print("Transforming order reviews...")

        silver_order_reviews = transform_order_reviews(
            source_data["order_reviews"]
        )

        print("Order reviews transformation completed.")

        print("Transforming geolocation...")

        silver_geolocation = transform_geolocation(
            source_data["geolocation"]
        )

        print("Geolocation transformation completed.")

        print("Transforming category translation...")

        silver_category_translation = transform_category_translation(
            source_data["category_translation"]
        )

        print("Category translation transformation completed.")

        print("Transforming order items...")

        silver_order_items = transform_order_items(
            source_data["order_items"]
        )

        print("Order items transformation completed.")

        print("Transforming order payments...")

        silver_order_payments = transform_order_payments(
            source_data["order_payments"]
        )

        print("Order payments transformation completed.")

        print("Transforming products...")

        silver_products = transform_products(source_data["products"])

        print("Products transformation completed.")

        print("Transforming sellers...")

        silver_sellers = transform_sellers(source_data["sellers"])

        print("Sellers transformation completed.")

        validate_core_silver_datasets(
            silver_customers,
            silver_orders,
            silver_order_reviews,
            len(source_data["customers"]),
            len(source_data["orders"]),
            len(source_data["order_reviews"]),
        )

        transformed_data = {
            "customers": silver_customers,
            "geolocation": silver_geolocation,
            "order_items": silver_order_items,
            "order_payments": silver_order_payments,
            "order_reviews": silver_order_reviews,
            "orders": silver_orders,
            "products": silver_products,
            "sellers": silver_sellers,
            "category_translation": silver_category_translation,
        }

        for name, dataframe in transformed_data.items():
            save_csv_to_s3(
                dataframe,
                S3_BUCKET,
                TARGET_FILES[name],
            )

        print("All nine Silver datasets were uploaded successfully.")
        return {
            "statusCode": 200,
            "body": {
                "message": "All transformations and uploads completed successfully.",
                "files": list(TARGET_FILES.values()),
            },
        }
    except Exception as error:
        print(f"Lambda execution failed: {error}")
        raise RuntimeError(
            f"Lambda execution aborted: {error}"
        ) from error
