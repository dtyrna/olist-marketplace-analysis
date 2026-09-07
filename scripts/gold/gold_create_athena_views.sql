--JOINED Tables order_payments, order_items, order_reviews, geolocation
--dropped unneccary id-columns
--change column's order to groups to a topic, e.g. delivery
--gave columns an Alias
CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.fact_orders AS
    SELECT
        o.order_id AS order_id,
        o.customer_id AS customer_id,
        o_i.product_id AS product_id,
        o_i.seller_id AS seller_id,
        o.order_status AS order_status,                
        o.order_purchase_timestamp AS purchase_timestamp,
        o.order_approved_at AS order_approved_at,
        o.order_estimated_delivery_date AS estimated_delivery_date,
        o.order_delivered_carrier_date AS delivered_carrier_date,
        o.order_delivered_customer_date AS delivered_customer_date,
        o_i.shipping_limit_date AS shipping_limit_date,
        o_i.freight_value AS freight_value,
        o_p.payment_installments AS payment_installments,
        o_p.payment_sequential AS payment_sequential,
        o_p.payment_type AS payment_type,
        o_p.payment_value AS payment_value,
        o_i.price AS product_price,
        o_r.review_score AS review_score,
        o_r.review_comment_title_en AS review_comment_title,
        o_r.review_comment_message_en AS review_comment_message,
        o_r.review_creation_date AS review_creation_date,
        o_r.review_answer_timestamp AS review_answer_timestamp
    FROM silver_csv_orders o
    LEFT JOIN silver_csv_order_payments o_p ON o.order_id = o_p.order_id
    LEFT JOIN silver_csv_order_items o_i ON o.order_id = o_i.order_id
    LEFT JOIN silver_csv_order_reviews o_r ON o.order_id = o_r.order_id
;

CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_products AS
    SELECT
        p.id_products AS id_products,
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
    LEFT JOIN category_translation ct ON p.product_category_name_bras = ct.product_category_name_bras
;



CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_customers AS
    SELECT
        -- c.id_customers AS id_customers, outlined for testing power bi connection
        c.customer_id AS customer_id,
        c.customer_unique_id AS customer_unique_id,
        c.customer_zip_code_prefix AS customer_zip_code_prefix,
        c.customer_city AS customer_city,
        c.customer_state AS customer_state,
        g.geolocation_lat AS geolocation_lat,
        g.geolocation_lng AS geolocation_lng 
    FROM silver_csv_customers c
    LEFT JOIN silver_csv_geolocation g ON silver_csv_customers.customer_zip_code_prefix = silver_csv_geolocation.geolocation_zip_code_prefix
;



CREATE OR REPLACE VIEW dsi_final_project_powerbi_dw.dim_sellers AS
    SELECT
        s.id_sellers AS id_sellers,
        s.seller_city AS seller_city,
        s.seller_id AS seller_id,
        s.seller_state AS seller_state,
        s.seller_zip_code_prefix AS seller_zip_code_prefix,
        g.geolocation_lat AS geolocation_lat,
        g.geolocation_lng AS geolocation_lng 
    FROM silver_csv_sellers s
    LEFT JOIN silver_csv_geolocation g ON silver_csv_sellers.seller_zip_code_prefix = silver_csv_geolocation.geolocation_zip_code_prefix
    ;