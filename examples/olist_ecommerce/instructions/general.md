# General Instructions - Olist E-Commerce

> Source of truth: repo. Edit this file, not the live room.

---

## Source Routing

- Use `workspace.olist_ecommerce.olist_order_metrics_mv` for order-level questions, monthly trends, raw counts, filters, city/state/category breakdowns, and delivery/review analysis that needs individual order rows.
- Use `workspace.olist_ecommerce.olist_category_diagnostics_mv` for product-category Pareto, contribution/share, late-delivery impact, review-score gap, and target-gap questions.
- Use `workspace.olist_ecommerce.olist_customer_state_diagnostics_mv` for customer-state Pareto, geographic contribution/share, late-delivery impact, review-score gap, and target-gap questions.

## Grain

One row per order. Use `order_id` as the order identifier.

## KPI Rules

- Total order value = `SUM(order_value)`.
- Total freight = `SUM(freight_value)`.
- Total payment value = `SUM(payment_value)`.
- Order count = `COUNT(DISTINCT order_id)`.
- Average review score = `AVG(review_score)` after filtering `has_review = true` when the question is specifically about reviews.
- Late delivery rate = `AVG(CASE WHEN is_late_delivery THEN 1 ELSE 0 END)`.
- Average delivery days = `AVG(delivery_days)`.
- Average days late = `AVG(days_late)`; use only delivered orders when discussing delivery lateness.
- Pareto/order-value concentration = use `cumulative_order_value_share` and `pareto_order_value_bucket` from the category diagnostics table.
- Pareto/order-count concentration = use `cumulative_order_count_share` and `pareto_order_count_bucket` from the customer-state diagnostics table.
- "How X affects Y" questions about late delivery and review score should use `review_score_gap_late_vs_on_time`, `avg_review_when_late`, and `avg_review_when_on_time`.
- "To increase review score to 4.2" questions should use `review_4_2_target_status`, `late_delivery_rate_needed_for_4_2_review`, and `late_delivery_rate_reduction_gap_to_4_2_review`.
- If `review_4_2_target_status = 'cannot_reach_4_2_by_late_delivery_alone'`, explain that late-delivery reduction by itself is not enough because even on-time orders average below 4.2.

## Date Logic

- Primary date column: `purchase_date`.
- Month grouping column: `purchase_month`.
- Use half-open date boundaries: `>= start AND < end_exclusive`.
- Avoid hardcoded dates unless the user explicitly asks for a historical calendar period from the dataset.
- The Olist dataset is historical. If users ask "latest" or "current", interpret it as the latest available period in the dataset and say so in the answer.

## Dimension Rules

- Customer geography uses `customer_state` and `customer_city`.
- Seller geography uses `seller_state` and `seller_city`.
- Product category uses `product_category`.
- Use `ILIKE` for free-text category/city filters.

## Output Conventions

- Top, bottom, highest, lowest, best, worst: default `LIMIT 5` unless the user gives a number.
- Always include the grouping dimension in the SELECT output.
- For rates, return decimals and a percent-friendly alias, for example `late_delivery_rate`.
- For monetary values, round to 2 decimals.
- For Pareto questions, include rank, share, cumulative share, and the Pareto bucket.
- For target-gap questions, include current rate, required target rate, and the reduction gap.
- For target feasibility questions, include `review_4_2_target_status`.
