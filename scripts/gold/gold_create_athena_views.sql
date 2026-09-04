CREATE OR REPLACE VIEW dim_customer AS
SELECT
  customer_id,
  customer_unique_id,
  customer_zip_code_prefix,
  customer_city,
  customer_state
FROM customers;

CREATE OR REPLACE VIEW dim_product AS
SELECT
  product_id,
  product_category_name,
  product_name_lenght,
  product_description_lenght,
  product_photos_qty,
  product_weight_g,
  product_length_cm,
  product_height_cm,
  product_width_cm
FROM products;

CREATE OR REPLACE VIEW dim_seller AS
SELECT
  seller_id,
  seller_zip_code_prefix,
  seller_city,
  seller_state
FROM sellers;

CREATE OR REPLACE VIEW fact_orders AS
SELECT
  order_id,
  customer_id,
  order_status,
  order_purchase_timestamp,
  order_approved_at,
  order_delivered_customer_date,
  order_delivered_carrier_date,
  order_estimated_delivery_date
FROM orders;

CREATE OR REPLACE VIEW fact_order_items AS
SELECT
  order_item_id,
  order_id,
  order_item_number,
  product_id,
  seller_id,
  shipping_limit_date,
  price,
  freight_value
FROM order_items;

CREATE OR REPLACE VIEW fact_order_payments AS
SELECT
  order_id,
  payment_sequential,
  payment_type,
  payment_installments,
  payment_value
FROM order_payments;

CREATE OR REPLACE VIEW fact_order_reviews AS
SELECT
  review_id,
  order_id,
  review_score,
  review_comment_title,
  review_comment_message,
  review_creation_date,
  review_answer_timestamp
FROM order_reviews;