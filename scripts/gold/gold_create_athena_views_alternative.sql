CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_date AS
WITH calendar AS (
    SELECT
        CAST(calendar_date AS DATE) AS full_date
    FROM UNNEST(
        sequence(
            TIMESTAMP '2016-01-01 00:00:00',
            TIMESTAMP '2020-12-31 00:00:00',
            INTERVAL '1' DAY
        )
    ) AS t(calendar_date)
)
SELECT
    CAST(date_format(full_date, '%Y%m%d') AS INTEGER) AS date_key,
    full_date,

    year(full_date) AS calendar_year,

    quarter(full_date) AS quarter_no,
    CONCAT('Q', CAST(quarter(full_date) AS VARCHAR)) AS quarter_name,
    CONCAT(
        CAST(year(full_date) AS VARCHAR),
        '-Q',
        CAST(quarter(full_date) AS VARCHAR)
    ) AS year_quarter_name,

    month(full_date) AS month_no,
    date_format(full_date, '%M') AS month_name,

    CAST(date_format(full_date, '%Y%m') AS INTEGER) AS year_month_key,
    date_format(full_date, '%Y-%m') AS year_month_name,

    week(full_date) AS iso_week_no,
    year_of_week(full_date) AS iso_week_year,
    CONCAT(
        CAST(year_of_week(full_date) AS VARCHAR),
        '-KW',
        LPAD(CAST(week(full_date) AS VARCHAR), 2, '0')
    ) AS iso_year_week_name,

    day_of_week(full_date) AS iso_weekday_no,
    date_format(full_date, '%W') AS weekday_name,

    CASE
        WHEN day_of_week(full_date) IN (6, 7) THEN TRUE
        ELSE FALSE
    END AS is_weekend,

    date_trunc('month', full_date) AS month_start_date,

    date_add(
        'day',
        -1,
        date_add('month', 1, date_trunc('month', full_date))
    ) AS month_end_date,

    date_trunc('quarter', full_date) AS quarter_start_date,

    date_add(
        'day',
        -1,
        date_add('quarter', 1, date_trunc('quarter', full_date))
    ) AS quarter_end_date

FROM calendar;

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_orders AS
    SELECT
        id_orders AS order_key,
        order_id,
        customer_id,
        order_status,
        CAST(
                date_format(CAST(order_purchase_timestamp AS DATE), '%Y%m%d')
                AS INTEGER
            ) AS purchase_date_key,

            CAST(
                date_format(CAST(order_approved_at AS DATE), '%Y%m%d')
                AS INTEGER
            ) AS approval_date_key,

            CAST(
                date_format(CAST(order_delivered_carrier_date AS DATE), '%Y%m%d')
                AS INTEGER
            ) AS carrier_date_key,

            CAST(
                date_format(CAST(order_delivered_customer_date AS DATE), '%Y%m%d')
                AS INTEGER
            ) AS delivered_date_key,

            CAST(
                date_format(CAST(order_estimated_delivery_date AS DATE), '%Y%m%d')
                AS INTEGER
            ) AS estimated_delivery_date_key,
        order_purchase_timestamp,
        order_approved_at,
        order_delivered_carrier_date,
        order_delivered_customer_date,
        order_estimated_delivery_date,
        carrier_before_purchase_flag,
        delivery_before_carrier_flag,
        missing_approval_flag,
        missing_carrier_date_flag,
        missing_delivery_date_flag
    FROM silver_csv_orders
;

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.fact_order_items AS
    SELECT
        id_olist_order_items AS order_item_key,
        order_id,
        product_id,
        seller_id,
        CAST(
            date_format(CAST(shipping_limit_date AS DATE), '%Y%m%d')
            AS INTEGER
        ) AS shipping_limit_date_key,
        order_item_id,
        price,
        freight_value
    FROM silver_csv_order_items
;

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.fact_order_reviews AS
    SELECT
        id_order_reviews AS review_key,
        review_id,
        order_id,
        CAST(
            date_format(CAST(review_creation_date AS DATE), '%Y%m%d')
            AS INTEGER
        ) AS review_creation_date_key,
        CAST(
            date_format(CAST(review_answer_timestamp AS DATE), '%Y%m%d')
            AS INTEGER
        ) AS review_answer_date_key,
        review_score,
        review_comment_title_en,
        review_comment_message_en
    FROM silver_csv_order_reviews_en
;

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.fact_order_payments AS
    SELECT
        p.id_order_payments AS payment_key,
        p.order_id,
        CAST(
            date_format(
                CAST(o.order_purchase_timestamp AS DATE),
                '%Y%m%d'
            ) AS INTEGER
        ) AS order_purchase_date_key,
        p.payment_sequential,
        p.payment_installments,
        p.payment_type,
        p.payment_value
    FROM silver_csv_order_payments p
    INNER JOIN silver_csv_orders o ON p.order_id = o.order_id
;

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_products AS
    SELECT
        p.id_products AS product_key,
        p.product_description_lenght AS product_description_lenght,
        p.product_height_cm AS product_height_cm,
        p.product_id AS product_id,
        p.product_length_cm AS product_length_cm,
        p.product_name_lenght AS product_name_lenght,
        p.product_photos_qty AS product_photos_qty,
        p.product_weight_g AS product_weight_g,
        p.product_width_cm AS product_width_cm,
        ct.product_category_name_eng AS product_category_name
    FROM silver_csv_products p
    LEFT JOIN silver_csv_category_translation ct ON p.product_category_name_bras = ct.product_category_name
;

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_customers AS
    SELECT
        c.id_customers AS customer_key,
        c.customer_id AS customer_id,
        c.customer_unique_id AS customer_unique_id,
        c.customer_zip_code_prefix AS customer_zip_code_prefix,
        c.customer_city AS customer_city,
        c.customer_state AS customer_state,
        g.geolocation_lat AS geolocation_lat,
        g.geolocation_lng AS geolocation_lng 
    FROM silver_csv_customers c
    LEFT JOIN silver_csv_geolocation g ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
;

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_sellers AS
    SELECT
        s.id_sellers AS seller_key,
        s.seller_city AS seller_city,
        s.seller_id AS seller_id,
        s.seller_state AS seller_state,
        s.seller_zip_code_prefix AS seller_zip_code_prefix,
        g.geolocation_lat AS geolocation_lat,
        g.geolocation_lng AS geolocation_lng 
    FROM silver_csv_sellers s
    LEFT JOIN silver_csv_geolocation g ON s.seller_zip_code_prefix = g.geolocation_zip_code_prefix
;

--create seperate dim_date per date-column for Power BI Semantic Model

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_purchase_date AS
    SELECT *
    FROM dsi_final_project_powerbi_dw.dim_date
;

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_delivery_date AS
    SELECT *
    FROM dsi_final_project_powerbi_dw.dim_date
;

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_review_date AS
    SELECT *
    FROM dsi_final_project_powerbi_dw.dim_date
;

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_shipping_limit_date AS
    SELECT *
    FROM dsi_final_project_powerbi_dw.dim_date
;