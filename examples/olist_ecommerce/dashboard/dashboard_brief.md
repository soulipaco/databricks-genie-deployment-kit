# AI/BI Dashboard Brief - Olist E-Commerce

Published dashboard:

[Open the live dashboard](https://dbc-5a674036-8eaa.cloud.databricks.com/dashboardsv3/01f173eb9b821ef9b5cf8e6c8ec78028/published?o=7474648785966975)

The published demo contains 29 interactive widgets across 8 pages. It is shared as run-as-owner so external portfolio reviewers can explore the dashboard without their own Databricks permissions.

## Audience

Marketplace operations, commercial leadership, and customer experience stakeholders.

## Dashboard Pages

### 1. Executive Overview

- KPI tiles: order value, order count, average review score, late delivery rate, average delivery days
- Monthly order value trend
- Monthly order count trend
- Top 5 product categories by order value

### 2. Delivery Performance

- Late delivery rate by month
- Late delivery rate by customer state
- Average delivery days by seller state
- Table: categories with highest late delivery rate and order count

### 3. Customer Experience

- Average review score by month
- Review score distribution
- Average review score by product category
- Scatter: late delivery rate vs average review score by category

### 4. Commercial Mix

- Order value by product category
- Freight as percent of order value by category
- Payment value by month
- Customer state contribution to order value

### 5. Diagnostic Prioritization

- Pareto product categories by cumulative order value share
- High-value categories with high late delivery rate
- Late vs on-time review score gap by product category
- Categories where late-delivery reduction can help reach a 4.2 review target
- Customer states in the Pareto top 80 percent of order volume

### 6. Playbook-Ready Action Planning

- Priority categories by value share and late delivery rate
- Categories where late delivery strongly affects review score
- Target-gap cases where delivery fixes can or cannot reach 4.2
- Fields designed to feed generated action-plan prompts

### 7. Data Quality and Governance

- Row counts and date coverage
- Payment reconciliation gap checks
- Review availability flags
- Operational buckets used consistently by dashboard, Genie, and playbook

### 8. Publication View

- Portfolio-ready summary pages
- Demo-friendly executive KPIs
- Charts that connect dashboard diagnostics to Genie questions
- Playbook references for moving from insight to action

## Suggested Genie Questions

- What product categories have the highest late delivery rate?
- Which customer states have the lowest average review score?
- Did late deliveries receive lower review scores?
- What was total order value by month?
- Which seller states have the highest average delivery time?
- Which product categories make up the top 80 percent of order value?
- How does late delivery affect review score by product category?
- To reach a 4.2 average review score, which categories need the largest late delivery rate reduction?
