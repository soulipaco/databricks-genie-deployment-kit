# Olist E-Commerce Operations Analytics - Action Playbook

Generated draft playbook for retrieval-augmented action planning.

- Source room: `Olist E-Commerce Operations Analytics`
- Generated from: `olist_ecommerce_deployment_kit`
- Purpose: Action plan playbook for the Olist e-commerce operations demo. Generated from the deployment kit metadata, enriched diagnostic tables, and Genie operating rules.
- Important: This is a generated draft and should be SME-reviewed before production use.

## 1) Room Source Reference and Interpretation Rules

### Olist E-Commerce Operations

- Question category: `olist_operations`
- Metric view: `workspace.olist_ecommerce.olist_order_metrics_mv`
- Underlying source: `workspace.olist_ecommerce.olist_order_metrics_mv`
- Grain: See KNOWLEDGE_BASE.md Source Table section.
- Core measures: `item_count`, `seller_count`, `order_value`, `freight_value`, `payment_value`, `review_score`, `delivery_days`, `days_late`
- Core dimensions: `order_id`, `customer_id`, `order_status`, `purchase_date`, `purchase_month`, `customer_city`, `customer_state`, `seller_city`
- Likely filters: `order_id`, `customer_id`, `order_status`, `customer_city`, `customer_state`, `seller_city`, `seller_state`, `product_category`
- Time columns: `purchase_date`

## 2) Domain Scenario Playbooks

### Olist E-Commerce Operations

**Domain:** Olist E-Commerce Operations

**Symptoms and analytical cues**
- Look first at `item_count`, `seller_count`, `order_value`, `freight_value`, `payment_value`.
- Cut by `order_id`, `customer_id`, `order_status`, `customer_city`, `customer_state`.
- Trend on `purchase_date`.

## 3) Recommendation Templates

These vector-friendly action cards are intended to be retrieved directly by the action-plan pipeline.

### Action Card: Olist E-Commerce Operations Fast Containment

- Category: `olist_operations`

## 4) Putting It Together: Example Recommended Plans
