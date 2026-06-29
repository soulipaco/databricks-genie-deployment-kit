# General Instructions

> **Room:** {{ROOM_NAME}}
> **Source of truth:** repo. Edit this file — do not edit the live room directly.

---

## Source Routing

{{DESCRIBE_WHICH_TABLES_TO_USE_FOR_WHICH_QUESTION_TYPES}}

## Grain Rules

{{DESCRIBE_THE_GRAIN_OF_EACH_TABLE_WHAT_ONE_ROW_REPRESENTS}}

## Date Logic

- Date column: `{{DATE_COLUMN}}`
- Default trend window: {{DEFAULT_WINDOW}}
- last month: `ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), -1)` to `DATE_TRUNC('MONTH', CURRENT_DATE())`
- this month: `DATE_TRUNC('MONTH', CURRENT_DATE())` to `CURRENT_DATE()`
- Always use half-open boundaries: `>= start AND < end_exclusive`
- NEVER hardcode dates — always use CURRENT_DATE() expressions

## Aggregation Rules

{{DESCRIBE_MEASURE_VS_RAW_AGGREGATION_RULES_FOR_EACH_TABLE}}

## Output Conventions

- top / bottom / highest / lowest → default LIMIT 5
- Always include filtered dimensions in SELECT output
- Text filters: always `ILIKE '%value%'`
