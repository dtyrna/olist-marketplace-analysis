USE dsi_final_project_powerbi_dw;

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_category_translation (
  category_id   STRING,
  category_name STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/category_translation/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);


CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_customers (
  customer_id           STRING,
  customer_unique_id    STRING,
  customer_zip_code_prefix STRING,
  customer_city         STRING,
  customer_state        STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/customers/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);


CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_geolocation (
  geolocation_zip_code_prefix STRING,
  geolocation_lat             DOUBLE,
  geolocation_lng             DOUBLE,
  geolocation_city            STRING,
  geolocation_state           STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/geolocation/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);


CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_order_items (
  order_item_id        STRING,
  order_id             STRING,
  order_item_number    INT,
  product_id           STRING,
  seller_id            STRING,
  shipping_limit_date  STRING,
  price                DOUBLE,
  freight_value        DOUBLE
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/order_items/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_order_payments (
  order_id              STRING,
  payment_sequential    INT,
  payment_type          STRING,
  payment_installments  INT,
  payment_value         DOUBLE
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/order_payments/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_order_reviews (
  review_id                 STRING,
  order_id                  STRING,
  review_score              INT,
  review_comment_title      STRING,
  review_comment_message    STRING,
  review_creation_date      STRING,
  review_answer_timestamp   STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/order_reviews/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_orders (
  order_id                        STRING,
  customer_id                     STRING,
  order_status                    STRING,
  order_purchase_timestamp        STRING,
  order_approved_at               STRING,
  order_delivered_customer_date   STRING,
  order_delivered_carrier_date    STRING,
  order_estimated_delivery_date   STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/orders/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_products (
  product_id                STRING,
  product_category_name     STRING,
  product_name_lenght       INT,
  product_description_lenght INT,
  product_photos_qty        INT,
  product_weight_g          INT,
  product_length_cm         INT,
  product_height_cm         INT,
  product_width_cm          INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/products/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_sellers (
  seller_id              STRING,
  seller_zip_code_prefix STRING,
  seller_city            STRING,
  seller_state           STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/sellers/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);