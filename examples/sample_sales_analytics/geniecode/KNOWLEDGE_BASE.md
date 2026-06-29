# GenieCode Knowledge Base — sample_sales_analytics
> **Last updated:** 2026-06-19
> **Purpose:** Single-file fast-context-load for AI coding agents. Read this FIRST every session.

## Room Identity
- **Room name:** sample_sales_analytics
- **Kit root:** examples/sample_sales_analytics/
- **Source of truth:** repo

## Capacity
- **Max room instructions:** 100
- **Active example_sql budget:** 98 (100 - 1 general - 1 table)
- **Active filters cap:** 100
- **Active measures cap:** 100

## Source Routing Table
| Domain | Table | Date Col | LOB Col |
|--------|-------|----------|---------|
| Revenue Performance | `sample_catalog.analytics_schema.sales_performance_mv` | `month_start_date` | `region` |

## Question-to-Source Routing
| Keywords | Route to |
|---------|----------|
| revenue, pipeline, close rate, deal, account, manager, region, product tier | `sales_performance_mv` |

## Date Logic
| Phrase | Logic |
|--------|-------|
| last month | `>= ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), -1) AND < DATE_TRUNC('MONTH', CURRENT_DATE())` |
| this month | `>= DATE_TRUNC('MONTH', CURRENT_DATE()) AND < CURRENT_DATE()` |
| last 6 months (incl. current) | `>= ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), -5) AND < ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), 1)` |
| last 12 weeks | `>= DATE_SUB(DATE_TRUNC('WEEK', CURRENT_DATE()), 84) AND < DATE_TRUNC('WEEK', CURRENT_DATE())` |

## Key Asset Counts
| Asset | Count |
|-------|-------|
| Benchmarks | 5 |
| Active example_sql | 3 |
| Active filters | 3 |
| Active measures | 3 |
| Library example_sql | 3 |

## Top Failure Modes
1. Wrong date column (use `month_start_date`, not `created_at` or `date`)
2. Calendar month vs rolling 30 days
3. SUM instead of MEASURE() for KPIs
4. Missing ILIKE for text dimension filters
5. Missing GROUP BY ALL when using MEASURE()
