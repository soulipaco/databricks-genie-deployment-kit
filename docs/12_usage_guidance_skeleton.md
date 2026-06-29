# 12 — Usage Guidance Skeleton

Skeleton for authoring the `usage_guidance` field in example_sql files.

```yaml
usage_guidance: |
  TRIGGER PHRASES:
    Use this example when the question asks for:
    - "<trigger phrase 1>"
    - "<trigger phrase 2>"
    - "<trigger phrase 3>"
    Common forms: "<natural language variants>"

  DATE BINDING (when using date parameters):
    StartDate = <start date formula, e.g. ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), -1)>
    EndDateExclusive = <end date formula, e.g. DATE_TRUNC('MONTH', CURRENT_DATE())>
    Anti-pattern: Do NOT exclude the current month.

  MANDATORY OUTPUT CONTRACT:
    The output MUST include:
    - <required column 1>
    - <required column 2>
    - <required column 3>
    The output MUST NOT include: <list forbidden columns>

  MANDATORY ANTI-PATTERNS:
    Do NOT <what to avoid 1>.
    Do NOT <what to avoid 2>.
    Do NOT use <wrong pattern> — use <correct pattern> instead.
```

## When to Add Each Field

| Field | When to add |
|-------|-------------|
| TRIGGER PHRASES | Always — prevents retrieval collision |
| DATE BINDING | Whenever using `:StartDate`/`:EndDateExclusive` parameters |
| MANDATORY OUTPUT CONTRACT | For complex examples with specific required columns |
| MANDATORY ANTI-PATTERNS | Whenever there is a simpler but wrong alternative |
