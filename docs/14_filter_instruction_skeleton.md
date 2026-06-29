# 14 — Filter Instruction Skeleton

Skeleton for authoring the `instruction` field in filter snippet files.

```yaml
instruction: |
  WHEN_TO_USE:
    Apply this filter when the user wants to restrict data to a specific <dimension_name>.
    Trigger phrases: "in <dimension>", "for <dimension>", "filtered by <dimension>",
    "where <dimension> is", "only <dimension> data".

  SCOPE_TABLES:
    This filter applies to: <table_identifier>.
    Do NOT apply to: <tables where this filter does not make sense>.

  TIMEFRAME_HINT:
    This filter can be applied to any time range. / This filter is only relevant for <time context>.

  RISK_IF_MISUSED:
    <What goes wrong if this filter is applied to the wrong table or in the wrong context>
    Example: "Applying this to <wrong_table> will return empty results because that table does not have <column>."
```

## Temporal Filter Instructions

For date/time filters, also include:
```
  DATE_LOGIC:
    Start boundary: <start_expression> (INCLUSIVE)
    End boundary: <end_expression> (EXCLUSIVE)
    Do NOT use BETWEEN — always use >= AND < for half-open boundaries.
```
