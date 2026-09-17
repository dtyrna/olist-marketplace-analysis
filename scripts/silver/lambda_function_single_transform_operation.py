import boto3
from io import BytesIO, StringIO

import numpy as np
import pandas as pd
from unidecode import unidecode


S3_BUCKET = "dsi-final-project-360964564955-eu-central-1-an"
SOURCE_PREFIX = "_raw/"
TARGET_PREFIX = "test/"


SOURCE_FILES = {
    "geolocation": "_raw/olist_geolocation_dataset.csv"
}


TARGET_FILES = {
    "geolocation": "test/geolocation/silver_geolocation.csv"
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



def lambda_handler(event, context):
    """Run the complete manual S3-to-S3 transformation workflow."""
    try:
        print("Lambda transformation started.")
        source_data = load_source_data()

        print("Transforming geolocation...")

        silver_geolocation = transform_geolocation(
            source_data["geolocation"]
        )

        print("Geolocation transformation completed.")

        

        transformed_data = {
            "geolocation": silver_geolocation
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
