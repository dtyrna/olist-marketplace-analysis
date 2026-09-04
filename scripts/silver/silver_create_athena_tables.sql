--###############################################
--Modify for real data
--###############################################

--###############################################
USE dsi_final_project_powerbi_dw;
--###############################################

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_category_translation (
  
  id_product_name_translation SMALLSERIAL,
  product_category_name_bras  VARCHAR,
  product_category_name_eng   VARCHAR
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/category_translation/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);


CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_customers (
  id_customers                BIGSERIAL,
  customer_id                 VARCHAR,
  customer_unique_id          VARCHAR,
  customer_zip_code_prefix    CHAR(5),
  customer_city               VARCHAR,
  customer_state              VARCHAR
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/customers/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);


CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_geolocation (
  id_geolocation                BIGSERIAL,
  geolocation_zip_code_prefix   VARCHAR
  geolocation_city              VARCHAR,
  geolocation_state             VARCHAR
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/geolocation/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);


CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_order_items (
  id_olist_order_items_dataset  BIGSERIAL,
  order_id                      VARCHAR,
  product_id                    VARCHAR(32),
  seller_id                     VARCHAR(32),
  shipping_limit_date           DATE,
  order_item_id                 SMALLINT,
  price                         FLOAT(5,2),
  freight_value                 FLOAT(5,2)
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/order_items/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_order_payments (
  id_order_payments     BIGSERIAL,
  order_id              CHAR(32),
  payment_installments  SMALLINT,
  payment_sequential    SMALLINT,
  payment_type          VARCHAR(20)
  payment_value         FLOAT(5,2)
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/order_payments/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_order_reviews (
  id_order_reviews            BIGSERIAL,
  review_id                   VARCHAR,
  order_id                    VARCHAR,
  review_score                SMALLINT,
  review_comment_title        VARCHAR,
  review_comment_title_en     VARCHAR,
  review_comment_message      VARCHAR,
  review_comment_message_en   VARCHAR,
  review_creation_date        DATE,
  review_answer_timestamp     DATE
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/order_reviews/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_orders (
  id_orders                       BIGSERIAL,
  order_id                        VARCHAR,
  customer_id                     VARCHAR,
  order_status                    CHAR(10),
  order_purchase_timestamp        DATE,
  order_approved_at               DATE,
  order_delivered_carrier_date    DATE,
  order_delivered_customer_date   DATE,
  order_estimated_delivery_date   DATE,
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/orders/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_products (
  id_products                 BIGSERIAL,
  product_category_name_bras  VARCHAR(50),
  product_description_lenght  INTEGER,
  product_height_cm           FLOAT(4,1),
  product_id                  CHAR(32),
  product_length_cm           FLOAT(4,1),
  product_name_lenght         INTEGER,
  product_photos_qty          SMALLINT,
  product_weight_g            FLOAT(4,1),
  product_width_cm            FLOAT(4,1)
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/products/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS silver.csv_sellers (
  id_sellers              BIGSERIAL,
  seller_city             VARCHAR(50),
  seller_id               CHAR(32),
  seller_state            CHAR(2),
  seller_zip_code_prefix  CHAR(5)
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/sellers/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);