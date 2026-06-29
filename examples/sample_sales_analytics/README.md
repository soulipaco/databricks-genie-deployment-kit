# Example: sample.sales Revenue Performance Room

Fully worked end-to-end example using the fictional company **sample.sales**.

## Room Overview

- **Room name:** `sample_sales_analytics`
- **Data source:** `sample_catalog.analytics_schema.sales_performance_mv` (metric view)
- **Grain:** One row per account per month
- **Primary KPI:** `MEASURE(monthly_revenue)`, `MEASURE(deal_close_rate)`, `MEASURE(pipeline_value)`
- **Dimensions:** `region`, `account_manager`, `product_tier`, `account_name`, `segment`

## What This Example Shows

- Complete `room.config.yml` with all fields populated
- 3 filter snippets (by region, by product tier, last month)
- 3 measure snippets (monthly revenue, deal close rate, pipeline value)
- 1 dimension snippet (period label)
- 3 example SQL entries (summary, trend, top-N)
- 5 benchmark questions with ground-truth SQL
- Activation manifests with specific IDs
- General instructions

## How to Use This Example

To create a new room based on this example:
1. Copy the files to a new kit directory
2. Replace all `sample_catalog.analytics_schema.*` references with your table
3. Replace all `sample_sales_analytics` references with your room name
4. Generate new IDs: `python -c "import uuid; print(uuid.uuid4().hex)"`
5. Update `env/local.yml` with your workspace credentials
6. Run `python scripts/validate.py`
