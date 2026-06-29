# 16 — Measure Instruction Skeleton

Skeleton for authoring the `instruction` field in measure snippet files.

```yaml
instruction: |
  WHEN_TO_USE:
    Use this measure to calculate <what it measures>.
    Trigger phrases: "what is the <measure name>", "<measure name> for",
    "calculate <measure name>", "show <measure name>".

  SCOPE_TABLES:
    This measure applies to: <table_identifier>.
    Do NOT use this measure with: <incompatible tables>.

  RISK_IF_MISUSED:
    <What goes wrong if this measure is misapplied>
    Example: "This measure is only valid at the <grain> level. Applying at a finer grain
    will produce inflated counts because <reason>."

  FORMATTING:
    Display as: <percentage / decimal / integer / currency>
    Format expression: <CONCAT/ROUND formula if applicable>
```

## When the Measure Uses MEASURE()

Add:
```
  MEASURE_CONTEXT:
    This is a semantic measure accessed via MEASURE(<column_name>).
    The metric view pre-computes <what it pre-computes> at <grain> level.
    Always use GROUP BY ALL when including this measure in a SELECT.
```
