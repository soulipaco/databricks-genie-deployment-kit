# General Instructions — sample_sales_analytics

> Source of truth: repo. Edit this file, not the live room.

---

## Source Routing

All queries use: `sample_catalog.analytics_schema.sales_performance_mv`

## Grain

One row per account per month. The date column is `month_start_date`.

## KPI Rules (Metric View)

- Always use `MEASURE(column_name)` for KPIs: `monthly_revenue`, `deal_close_rate`, `pipeline_value`, `deals_won`, `deals_lost`.
- Always use `GROUP BY ALL` when using `MEASURE()`.
- Use alias from SELECT in HAVING (not `MEASURE()`).

## Date Logic

- Date column: `month_start_date`
- Default trend: last 6 calendar months including current
- last month = `ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), -1)` to `DATE_TRUNC('MONTH', CURRENT_DATE())`
- this month = `DATE_TRUNC('MONTH', CURRENT_DATE())` to `CURRENT_DATE()`
- last N months (including current) = `ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), -(N-1))` to `ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), 1)`
- ALWAYS use half-open boundaries: `>= start AND < end_exclusive`
- NEVER use BETWEEN for date ranges
- NEVER hardcode dates — always use CURRENT_DATE() expressions

## Output Conventions

- Top / bottom / highest / lowest / best / worst → default LIMIT 5 (unless N specified)
- Percentage format: `CONCAT(ROUND(MEASURE(deal_close_rate) * 100, 2), '%')`
- Revenue format: `ROUND(MEASURE(monthly_revenue), 0)` (no decimals for revenue)
- Rank by descending by default for "top" questions
- Always include filtered dimensions in SELECT output

## Text Filters

- Always use `ILIKE '%value%'` for text dimension filters (region, account_manager, account_name, segment, product_tier)
- Never use `=` for text comparisons
