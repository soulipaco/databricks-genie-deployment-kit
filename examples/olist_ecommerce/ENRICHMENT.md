# Enrichment Layer

The Olist demo now includes diagnostic fields and aggregate tables for richer Genie questions.

## Order-Level Enrichment

Table: `workspace.olist_ecommerce.olist_order_metrics_mv`

Added fields:

- `freight_to_order_value_ratio`
- `payment_reconciliation_gap`
- `review_score_band`
- `order_value_band`
- `delivery_speed_band`
- `delivery_status_bucket`
- `delivery_review_segment`

Use this table for order-level trends, filters, and dashboard details.

## Product Category Diagnostics

Table: `workspace.olist_ecommerce.olist_category_diagnostics_mv`

Purpose:

- Pareto analysis by order value
- category contribution/share
- late-delivery rate by category
- late vs on-time review score gap
- target-gap modeling for reaching 4.2 average review score

Useful fields:

- `order_value_share`
- `cumulative_order_value_share`
- `pareto_order_value_bucket`
- `review_score_gap_late_vs_on_time`
- `review_4_2_target_status`
- `late_delivery_rate_needed_for_4_2_review`
- `late_delivery_rate_reduction_gap_to_4_2_review`

## Customer State Diagnostics

Table: `workspace.olist_ecommerce.olist_customer_state_diagnostics_mv`

Purpose:

- Pareto analysis by order count
- geographic contribution/share
- late-delivery and review-score diagnostics by customer state
- target-gap modeling for review-score improvement

Useful fields:

- `order_count_share`
- `cumulative_order_count_share`
- `pareto_order_count_bucket`
- `review_score_gap_late_vs_on_time`
- `review_4_2_target_status`
- `late_delivery_rate_needed_for_4_2_review`
- `late_delivery_rate_reduction_gap_to_4_2_review`

## New Genie Question Types

- Which product categories make up the top 80 percent of order value?
- How does late delivery affect review score by product category?
- To reach a 4.2 average review score, which categories need the largest late delivery rate reduction?
- Which customer states drive the Pareto top 80 percent of order volume?
- Which product categories combine high order value share and high late delivery rate?

