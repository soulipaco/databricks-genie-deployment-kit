# Semantic Contract — {{TABLE_DISPLAY_NAME}}

> **Table:** `{{CATALOG}}.{{SCHEMA}}.{{TABLE_NAME}}`
> **Last reviewed:** {{DATE}}

## Grain

**One row represents:** {{GRAIN_DESCRIPTION}}
**Date column:** `{{DATE_COLUMN}}`
**Identity column(s):** `{{IDENTITY_COLUMNS}}`

## Semantic Measures

Access all KPIs via `MEASURE(column_name)` with `GROUP BY ALL`.

| Measure Column | Display Name | Formula/Definition | Grain Restriction |
|---------------|--------------|-------------------|-------------------|
| `{{MEASURE_1}}` | {{DISPLAY_1}} | {{DEFINITION_1}} | {{RESTRICTION_1}} |
| `{{MEASURE_2}}` | {{DISPLAY_2}} | {{DEFINITION_2}} | {{RESTRICTION_2}} |

## Aggregation Rules

1. {{RULE_1}}
2. {{RULE_2}}

## Date Logic

- Date column: `{{DATE_COLUMN}}`
- Default window: {{DEFAULT_WINDOW}}
- Use half-open boundaries: `>= start AND < end_exclusive`

## Scope Restrictions

{{SCOPE_RESTRICTIONS}}
