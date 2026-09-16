USE dsi_final_project_powerbi_dw;

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_category_translation;

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_category_translation (
  product_category_name  STRING,
  product_category_name_eng   STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/category_translation/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_customers;

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
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/customers/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_geolocation;

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_geolocation (
  id_geolocation                BIGINT,
  geolocation_zip_code_prefix   STRING,
  geolocation_lat               DOUBLE,
  geolocation_lng               DOUBLE,
  geolocation_city              STRING,
  geolocation_state             STRING
  
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/geolocation/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_order_items;

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_order_items (
  id_olist_order_items          BIGINT,
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
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/order_items/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_order_payments;

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
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/order_payments/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_order_reviews_en;

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_order_reviews_en (
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
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/order_reviews/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_orders;

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_orders (
  id_orders                       BIGINT,
  order_id                        STRING,
  customer_id                     STRING,
  order_status                    STRING,
  order_purchase_timestamp        TIMESTAMP,
  order_approved_at               TIMESTAMP,
  order_delivered_carrier_date    TIMESTAMP,
  order_delivered_customer_date   TIMESTAMP,
  order_estimated_delivery_date   DATE,
  carrier_before_purchase_flag    BOOLEAN,
  delivery_before_carrier_flag    BOOLEAN,
  missing_approval_flag           BOOLEAN,
  missing_carrier_date_flag       BOOLEAN,
  missing_delivery_date_flag      BOOLEAN
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/orders/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_products;

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
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/products/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_sellers;

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
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/sellers/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_comment_topics;

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_comment_topics (
  id_order_reviews            STRING,
  review_id                   STRING,
  order_id                    STRING,
  review_score                STRING,
  review_comment_message_en   STRING,
  topic                       STRING,
  is_negative                 STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar'     = '"',
  'escapeChar'    = '\\'
)
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/comment_topics/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_topic_analysis;

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_topic_analysis (
  topic                       STRING,
  review_count                INTEGER,
  share_pct                   DOUBLE,
  negative_reviews            INTEGER,
  negative_rate_pct           DOUBLE,
  avg_review_score            DOUBLE,
  negative_contribution_pct   DOUBLE,
  priority_score              INTEGER
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/topic_analysis/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

DROP TABLE IF EXISTS dsi_final_project_powerbi_dw.silver_csv_topic_score_distribution;

CREATE EXTERNAL TABLE IF NOT EXISTS dsi_final_project_powerbi_dw.silver_csv_topic_score_distribution (
  topic           STRING,
  review_score    INTEGER,
  review_count    INTEGER,
  score_share     DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://dsi-final-project-360964564955-eu-central-1-an/_processed/topic_score_distribution/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);