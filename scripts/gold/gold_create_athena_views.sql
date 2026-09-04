--JOINED Tables order_payments, order_items, order_reviews
--dropped unneccary id-columns
--change column's order to groups to a topic, e.g. delivery
--gave columns an Alias
CREATE OR REPLACE VIEW gold.fact_orders AS
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
    FROM orders o
    LEFT JOIN order_payments o_p ON o.order_id = o_p.order_id
    LEFT JOIN order_items o_i ON o.order_id = o_i.order_id
    LEFT JOIN order_reviews o_r ON o.order_id = o_r.order_id
;

CREATE OR REPLACE VIEW gold.dim_products AS
    SELECT
        p.id_products,
        p.product_description_lenght,
        p.product_height_cm,
        p.product_id,
        p.product_length_cm,
        p.product_name_lenght,
        p.product_photos_qty,
        p.product_weight_g,
        p.product_width_cm
        ct.product_category_name_eng
    FROM products p
    LEFT JOIN category_translation ct ON p.product_category_name_bras = ct.product_category_name_bras
;



CREATE OR REPLACE VIEW gold.dim_customer AS
    SELECT
        id_customers,
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state   
    FROM customers
;



CREATE OR REPLACE VIEW gold.dim_seller AS
    SELECT
        id_sellers,
        seller_city,
        seller_id,
        seller_state,
        seller_zip_code_prefix
    FROM sellers;