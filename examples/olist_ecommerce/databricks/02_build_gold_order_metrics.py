# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Build Gold Order Metrics
# MAGIC
# MAGIC Creates `olist_order_metrics_mv`, the single Genie-ready table used by the room and dashboard.

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text("schema", "olist_ecommerce")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

if "{{" in catalog or "{{" in schema:
    raise ValueError("Replace widget placeholders before running this notebook.")

spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"USE SCHEMA {schema}")

gold_table = f"{catalog}.{schema}.olist_order_metrics_mv"
print(f"Building {gold_table}")

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE {gold_table} AS
WITH order_items AS (
  SELECT
    oi.order_id,
    COUNT(*) AS item_count,
    COUNT(DISTINCT oi.seller_id) AS seller_count,
    ROUND(SUM(CAST(oi.price AS DOUBLE)), 2) AS order_value,
    ROUND(SUM(CAST(oi.freight_value AS DOUBLE)), 2) AS freight_value,
    MIN(oi.seller_id) AS primary_seller_id,
    MIN(oi.product_id) AS primary_product_id,
    MIN(CAST(oi.shipping_limit_date AS TIMESTAMP)) AS first_shipping_limit_ts
  FROM {catalog}.{schema}.bronze_olist_order_items oi
  GROUP BY oi.order_id
),
payments AS (
  SELECT
    op.order_id,
    ROUND(SUM(CAST(op.payment_value AS DOUBLE)), 2) AS payment_value,
    COUNT(*) AS payment_installment_rows,
    MAX(CAST(op.payment_installments AS INT)) AS max_payment_installments
  FROM {catalog}.{schema}.bronze_olist_order_payments op
  GROUP BY op.order_id
),
reviews AS (
  SELECT
    ore.order_id,
    ROUND(AVG(CAST(ore.review_score AS DOUBLE)), 2) AS review_score,
    COUNT(*) AS review_count
  FROM {catalog}.{schema}.bronze_olist_order_reviews ore
  GROUP BY ore.order_id
),
products AS (
  SELECT
    p.product_id,
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS product_category
  FROM {catalog}.{schema}.bronze_olist_products p
  LEFT JOIN {catalog}.{schema}.bronze_product_category_translation t
    ON p.product_category_name = t.product_category_name
)
SELECT
  o.order_id,
  o.customer_id,
  o.order_status,
  CAST(o.order_purchase_timestamp AS TIMESTAMP) AS purchase_ts,
  CAST(o.order_purchase_timestamp AS DATE) AS purchase_date,
  DATE_TRUNC('MONTH', CAST(o.order_purchase_timestamp AS DATE)) AS purchase_month,
  CAST(o.order_approved_at AS TIMESTAMP) AS approved_ts,
  CAST(o.order_delivered_carrier_date AS TIMESTAMP) AS delivered_carrier_ts,
  CAST(o.order_delivered_customer_date AS TIMESTAMP) AS delivered_customer_ts,
  CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_ts,

  c.customer_city,
  c.customer_state,
  s.seller_city,
  s.seller_state,
  pr.product_category,

  COALESCE(oi.item_count, 0) AS item_count,
  COALESCE(oi.seller_count, 0) AS seller_count,
  COALESCE(oi.order_value, 0.0) AS order_value,
  COALESCE(oi.freight_value, 0.0) AS freight_value,
  COALESCE(pay.payment_value, 0.0) AS payment_value,
  COALESCE(pay.payment_installment_rows, 0) AS payment_installment_rows,
  COALESCE(pay.max_payment_installments, 0) AS max_payment_installments,

  rev.review_score,
  COALESCE(rev.review_count, 0) AS review_count,
  CASE WHEN rev.review_count > 0 THEN true ELSE false END AS has_review,

  CASE
    WHEN o.order_delivered_customer_date IS NOT NULL
    THEN DATEDIFF(CAST(o.order_delivered_customer_date AS DATE), CAST(o.order_purchase_timestamp AS DATE))
  END AS delivery_days,
  CASE
    WHEN o.order_delivered_customer_date IS NOT NULL
    THEN GREATEST(DATEDIFF(CAST(o.order_delivered_customer_date AS DATE), CAST(o.order_estimated_delivery_date AS DATE)), 0)
  END AS days_late,
  CASE
    WHEN o.order_delivered_customer_date IS NOT NULL
     AND CAST(o.order_delivered_customer_date AS TIMESTAMP) > CAST(o.order_estimated_delivery_date AS TIMESTAMP)
    THEN true ELSE false
  END AS is_late_delivery
FROM {catalog}.{schema}.bronze_olist_orders o
LEFT JOIN order_items oi
  ON o.order_id = oi.order_id
LEFT JOIN payments pay
  ON o.order_id = pay.order_id
LEFT JOIN reviews rev
  ON o.order_id = rev.order_id
LEFT JOIN {catalog}.{schema}.bronze_olist_customers c
  ON o.customer_id = c.customer_id
LEFT JOIN {catalog}.{schema}.bronze_olist_sellers s
  ON oi.primary_seller_id = s.seller_id
LEFT JOIN products pr
  ON oi.primary_product_id = pr.product_id
""")

# COMMAND ----------

spark.sql(f"""
COMMENT ON TABLE {gold_table} IS
'Olist e-commerce order metrics. One row per order enriched with customer geography, seller geography, product category, payment totals, review score, delivery duration, and late-delivery indicators.'
""")

column_comments = {
    "order_id": "Unique order identifier.",
    "customer_id": "Customer identifier from the Olist dataset.",
    "order_status": "Order lifecycle status.",
    "purchase_date": "Date when the order was purchased.",
    "purchase_month": "Month of order purchase, used for trend analysis.",
    "customer_city": "Customer city.",
    "customer_state": "Customer Brazilian state.",
    "seller_city": "Primary seller city for the order.",
    "seller_state": "Primary seller Brazilian state for the order.",
    "product_category": "English product category for the primary product in the order.",
    "item_count": "Number of order item rows in the order.",
    "seller_count": "Number of distinct sellers in the order.",
    "order_value": "Sum of item price for the order, excluding freight.",
    "freight_value": "Sum of freight value for the order.",
    "payment_value": "Total payment value recorded for the order.",
    "review_score": "Average review score for the order.",
    "delivery_days": "Days between purchase and customer delivery.",
    "days_late": "Days delivered after estimated delivery date; zero when not late.",
    "is_late_delivery": "True when delivered after estimated delivery timestamp.",
    "has_review": "True when the order has at least one review row.",
}

for column_name, comment in column_comments.items():
    spark.sql(f"ALTER TABLE {gold_table} ALTER COLUMN {column_name} COMMENT '{comment}'")

# COMMAND ----------

display(spark.sql(f"""
SELECT
  COUNT(*) AS row_count,
  COUNT(DISTINCT order_id) AS order_count,
  MIN(purchase_date) AS min_purchase_date,
  MAX(purchase_date) AS max_purchase_date,
  ROUND(SUM(order_value), 2) AS total_order_value,
  ROUND(AVG(review_score), 2) AS average_review_score,
  ROUND(AVG(CASE WHEN is_late_delivery THEN 1 ELSE 0 END), 4) AS late_delivery_rate
FROM {gold_table}
"""))

