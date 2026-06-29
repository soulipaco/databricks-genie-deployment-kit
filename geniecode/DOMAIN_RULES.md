# Domain Rules — {{ROOM_NAME}}
> **Last updated:** {{UPDATE_DATE}}
> Distilled decision rules for SQL generation, validation, and benchmark evaluation.
> Update this file after every domain rule change or benchmark evaluation cycle.

---

## Universal Rules

### Text Filters
- Always use `ILIKE '%value%'` for text-based filters.
- Always include filtered dimensions in the SELECT output.

### Date Windows
- Use bounded half-open: `>= start AND < end_exclusive`.
- Parameter convention: `:StartDate` / `:EndDateExclusive`.
- `last month` = previous full calendar month.
- `this month` = current calendar month to date.
- `last week` = DATE_TRUNC('WEEK', CURRENT_DATE()) - 7 to DATE_TRUNC('WEEK', CURRENT_DATE()).
- `last N months` = calendar months INCLUDING current, NOT rolling N*30 days.
- Default trends: weekly = 12 weeks, monthly = 6 months including current.

### Period Grain Metadata
- Set `period_grain` to match the window: DAY / WEEK / MONTH.
- NEVER default `period_grain` to DAY for week/month windows.

### Result Limits
- Default top/bottom N = 5 (when user says "top", "bottom", "highest", "lowest", "best", "worst").

### People Identity
- Always include the primary identity column in output when filtering by person.
- Prefer the most stable identifier (e.g., employee_id) over display names.
- Cross-source joins: use the most stable common identifier.

---

## Domain 1: {{DOMAIN_1_NAME}} (`{{TABLE_1}}`)

### Grain Control (CRITICAL)
- {{TABLE_1_GRAIN_RULE}}
- KPI measures: use MEASURE() — do NOT recalculate from raw rows.

### Measure Rules
- {{DOMAIN_1_MEASURE_RULE_1}}
- {{DOMAIN_1_MEASURE_RULE_2}}

### Display Conventions
- {{DOMAIN_1_DISPLAY_CONVENTION_1}}
- {{DOMAIN_1_DISPLAY_CONVENTION_2}}

---

## Domain 2: {{DOMAIN_2_NAME}} (`{{TABLE_2}}`)

### Grain Control
- {{TABLE_2_GRAIN_RULE}}

### Measure Rules
- {{DOMAIN_2_MEASURE_RULE_1}}

---

## When to Use Metric View vs Raw Table
| Pattern | Use |
|---------|-----|
| Standard summary, ranking, comparison, trend | Metric view + MEASURE() |
| Pareto analysis on individual rows | Raw table |
| Leave-one-out / agent impact analysis | Raw table |
| Weighted KPI-row calculations | Raw table |
| Exclusive classification | Raw table |
