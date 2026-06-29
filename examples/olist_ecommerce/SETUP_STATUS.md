# Olist Demo Setup Status

Last updated: 2026-06-29

## Completed

- Downloaded the public Olist Brazilian E-Commerce dataset locally with `kagglehub`.
- Copied raw CSVs into `examples/olist_ecommerce/downloads/` locally.
- Uploaded all nine CSV files to the Databricks Volume:
  - `/Volumes/workspace/olist_ecommerce/olist_raw`
- Created schema:
  - `workspace.olist_ecommerce`
- Created managed volume:
  - `workspace.olist_ecommerce.olist_raw`
- Created bronze Delta tables for all source CSV files.
- Recreated the reviews bronze table with multiline CSV handling.
- Created the gold Genie/dashboard table:
  - `workspace.olist_ecommerce.olist_order_metrics_mv`
- Created a deployable Genie room package in this folder.
- Deployed the Olist Genie room successfully.
- Enriched the model with category and customer-state diagnostic tables for Pareto, driver-impact, and target-gap questions.

## Gold Table Validation

`workspace.olist_ecommerce.olist_order_metrics_mv`

- Row count: 99,441
- Distinct orders: 99,441
- Date range: 2016-09-04 to 2018-10-17
- Total order value: about 13.59M
- Average review score: 4.09
- Late delivery rate: 7.87%
- Product category diagnostic rows: 75
- Customer state diagnostic rows: 27

## Verified Query Themes

- Monthly order value trend
- Late delivery rate by product category
- Review score by customer state

## Next Steps

1. Open the deployed Genie room and run the sample questions.
2. Build the AI/BI dashboard from `dashboard/dashboard_brief.md`.
3. Capture screenshots for the GitHub README and LinkedIn portfolio post.
