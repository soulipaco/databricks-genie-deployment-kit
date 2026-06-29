# GenieCode Knowledge Base
> **Last updated:** {{UPDATE_DATE}}
> **Purpose:** Single-file fast-context-load for AI coding agents. Read this FIRST every session.

---

## Room Identity
- **Room name:** {{ROOM_NAME}}
- **Kit root:** {{KIT_ROOT_PATH}}
- **Source of truth:** repo (folder files override live room)
- **Deploy surface:** `instructions/` (materialized from `instruction_library/`)
- **Push script:** `scripts/push_folder_to_room.py`
- **Pull script:** `scripts/pull_room_to_folder.py`

## Capacity Limits
- **Max room instructions:** 100
- **Active example_sql budget:** {{EXAMPLE_SQL_BUDGET}} (100 - 1 general - N tables)
- **Active filters cap:** 100
- **Active measures cap:** 100

## Source Routing Table
| Domain | Table (metric view) | Date Col | LOB Col |
|--------|---------------------|----------|---------|
| {{DOMAIN_1}} | `{{CATALOG}}.{{SCHEMA}}.{{TABLE_1_MV}}` | `{{DATE_COL_1}}` | `{{LOB_COL_1}}` |
| {{DOMAIN_2}} | `{{CATALOG}}.{{SCHEMA}}.{{TABLE_2_MV}}` | `{{DATE_COL_2}}` | `{{LOB_COL_2}}` |

## Question-to-Source Routing Heuristic
| Keywords in question | Route to |
|---------------------|----------|
| {{KEYWORD_GROUP_1}} | {{DOMAIN_1}} |
| {{KEYWORD_GROUP_2}} | {{DOMAIN_2}} |

## Date Logic Quick Reference
| Phrase | Logic |
|--------|-------|
| yesterday | `>= DATE_SUB(CURRENT_DATE(), 1) AND < CURRENT_DATE()` |
| last week | `>= DATE_SUB(DATE_TRUNC('WEEK', CURRENT_DATE()), 7) AND < DATE_TRUNC('WEEK', CURRENT_DATE())` |
| this week | `>= DATE_TRUNC('WEEK', CURRENT_DATE()) AND < DATE_ADD(DATE_TRUNC('WEEK', CURRENT_DATE()), 7)` |
| last month | Previous full calendar month (half-open boundaries) |
| this month | Current calendar month to date |
| last N months | Calendar months INCLUDING current month |
| Default weekly trend | Last 12 weeks |
| Default monthly trend | Last 6 calendar months including current |

## Key Asset Counts
| Asset Type | Location | Count |
|------------|----------|-------|
| Benchmarks | `benchmarks/` | {{BENCHMARK_COUNT}} |
| Active example_sql | `instructions/example_sql/` | {{EXAMPLE_SQL_COUNT}} |
| Active filters | `instructions/sql_snippets/filters/` | {{FILTER_COUNT}} |
| Active measures | `instructions/sql_snippets/measures/` | {{MEASURE_COUNT}} |
| Active dimensions | `instructions/sql_snippets/dimensions/` | {{DIMENSION_COUNT}} |
| Library example_sql | `instruction_library/corpus/example_sql/` | {{LIBRARY_SQL_COUNT}} |

## Top 10 Failure Modes to Check
1. **Wrong source table** — question routed to wrong domain
2. **Wrong date column** — using wrong date/timestamp column for the table
3. **Wrong LOB column** — using wrong line-of-business column for the domain
4. **Grain violation** — mixing incompatible row levels in aggregation
5. **Semantic measure misuse** — using MEASURE() when raw rows needed or vice versa
6. **Date logic error** — rolling days instead of calendar months
7. **Wrong period grain metadata** — DAY when should be WEEK/MONTH
8. **Missing ILIKE** — text filters using `=` instead of `ILIKE`
9. **Missing output columns** — filtered dimensions not in SELECT
10. **Ranking inversion** — top/bottom (magnitude) vs best/worst (desirability)

## Snippet Health Check
- **Procedure:** `geniecode/SNIPPET_HEALTH_CHECK.md`
- **Script:** `geniecode/scripts/snippet_health_check.py`
  - Full scan: `python geniecode/scripts/snippet_health_check.py --mode full --fix-plan`
  - Single snippet: `python geniecode/scripts/snippet_health_check.py --mode single --target <alias>`
  - JSON output: `--output json`
  - Type filter: `--type filters|measures|dimensions`
