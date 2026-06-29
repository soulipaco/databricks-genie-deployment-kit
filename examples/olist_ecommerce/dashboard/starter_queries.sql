-- Replace workspace and olist_ecommerce before running.

-- Executive KPI tiles
SELECT
  ROUND(SUM(order_value), 2) AS total_order_value,
  COUNT(DISTINCT order_id) AS order_count,
  ROUND(AVG(review_score), 2) AS average_review_score,
  ROUND(AVG(CASE WHEN is_late_delivery THEN 1 ELSE 0 END), 4) AS late_delivery_rate,
  ROUND(AVG(delivery_days), 2) AS average_delivery_days
FROM workspace.olist_ecommerce.olist_order_metrics_mv;

-- Monthly order value
SELECT
  purchase_month,
  ROUND(SUM(order_value), 2) AS total_order_value,
  COUNT(DISTINCT order_id) AS order_count
FROM workspace.olist_ecommerce.olist_order_metrics_mv
GROUP BY purchase_month
ORDER BY purchase_month;

-- Category delivery and review diagnostics
SELECT
  product_category,
  COUNT(DISTINCT order_id) AS order_count,
  ROUND(SUM(order_value), 2) AS total_order_value,
  ROUND(AVG(CASE WHEN is_late_delivery THEN 1 ELSE 0 END), 4) AS late_delivery_rate,
  ROUND(AVG(review_score), 2) AS average_review_score
FROM workspace.olist_ecommerce.olist_order_metrics_mv
GROUP BY product_category
HAVING order_count >= 100
ORDER BY late_delivery_rate DESC
LIMIT 20;

