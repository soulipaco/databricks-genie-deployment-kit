# 05 — Metric View Contract Summary

## What Is a Metric View?

A Databricks metric view is a pre-computed semantic layer over raw data tables.
KPI values are stored as measure columns accessed via `MEASURE(measure_name)`.

## Contract Rules (per metric view)

### Rule 1: MEASURE() for KPIs
- Always use `MEASURE(column_name)` to access pre-computed KPI values
- Never recalculate KPIs from raw row math (e.g., dividing SUM() columns)
- Exception: when the metric view has no measure column for the needed KPI

### Rule 2: GROUP BY ALL
- Always use `GROUP BY ALL` when using `MEASURE()` in the SELECT
- Never list individual GROUP BY columns when using MEASURE()

### Rule 3: HAVING Alias
- Use the alias from the SELECT clause in HAVING, not `MEASURE()` directly
- Example: `SELECT MEASURE(kpi) AS score ... HAVING score > 0` (not `HAVING MEASURE(kpi) > 0`)

### Rule 4: Percentage Formatting
- Use `CONCAT(ROUND(MEASURE(kpi) * 100, 2), '%')` for rate/proportion KPIs
- Use `ROUND(MEASURE(kpi), 2)` for decimal values

### Rule 5: Grain Restrictions
- Some measures are pre-aggregated at a specific grain (e.g., agent-month level)
- Adding finer-grain dimensions will produce incorrect results
- Consult `geniecode/TABLE_SCHEMAS.md` for grain restrictions per table

## Semantic Contracts by Table

See `docs/contracts/` for full contracts per metric view.
