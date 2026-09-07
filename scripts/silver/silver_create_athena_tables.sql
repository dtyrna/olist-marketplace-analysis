--###############################################
--Modify for real data
--###############################################

--###############################################
USE dsi_final_project_powerbi_dw;
--###############################################

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_category_translation (
  id_product_name_translation INT,
  product_category_name_bras  STRING,
  product_category_name_eng   STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/category_translation/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);


CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_customers (
  id_customers                BIGINT,
  customer_id                 STRING,
  customer_unique_id          STRING,
  customer_zip_code_prefix    STRING,
  customer_city               STRING,
  customer_state              STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/customers/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);


CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_geolocation (
  id_geolocation                BIGINT,
  geolocation_zip_code_prefix   STRING
  geolocation_city              STRING,
  geolocation_state             STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/geolocation/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);


CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_order_items (
  id_olist_order_items_dataset  BIGINT,
  order_id                      STRING,
  product_id                    STRING,
  seller_id                     STRING,
  shipping_limit_date           DATE,
  order_item_id                 INT,
  price                         DECIMAL(5,2),
  freight_value                 DECIMAL(5,2)
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/order_items/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_order_payments (
  id_order_payments     BIGINT,
  order_id              STRING,
  payment_installments  INT,
  payment_sequential    INT,
  payment_type          STRING,
  payment_value         DECIMAL(5,2)
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/order_payments/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_order_reviews (
  id_order_reviews            BIGINT,
  review_id                   STRING,
  order_id                    STRING,
  review_score                INT,
  review_comment_title        STRING,
  review_comment_title_en     STRING,
  review_comment_message      STRING,
  review_comment_message_en   STRING,
  review_creation_date        DATE,
  review_answer_timestamp     TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/order_reviews/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_orders (
  id_orders                       BIGINT,
  order_id                        STRING,
  customer_id                     STRING,
  order_status                    STRING,
  order_purchase_timestamp        TIMESTAMP,
  order_approved_at               DATE,
  order_delivered_carrier_date    DATE,
  order_delivered_customer_date   DATE,
  order_estimated_delivery_date   DATE,
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/orders/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_products (
  id_products                 BIGINT,
  product_category_name_bras  STRING,
  product_description_lenght  INTEGER,
  product_height_cm           DECIMAL(4,1),
  product_id                  STRING,
  product_length_cm           DECIMAL(4,1),
  product_name_lenght         INTEGER,
  product_photos_qty          INT,
  product_weight_g            DECIMAL(4,1),
  product_width_cm            DECIMAL(4,1)
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/products/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_sellers (
  id_sellers              BIGINT,
  seller_city             STRING,
  seller_id               STRING,
  seller_state            STRING,
  seller_zip_code_prefix  STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
--###############################################
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/test/sellers/'
--###############################################
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);