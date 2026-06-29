# Active Example SQL — Deploy Surface

This directory is the active deploy surface for example SQL entries.
It is materialized from `instruction_library/corpus/example_sql/` by `scripts/materialize.py`.

**Do NOT add files here directly.** Always author in `instruction_library/corpus/example_sql/` first.

## Format

```yaml
id: <32-char hex>
question: <natural language question>
sql: <SQL query>
parameters:            # Optional
  - name: StartDate
    type_hint: DATE
usage_guidance: |     # Optional
  TRIGGER PHRASES: ...
  DATE BINDING: ...
  MANDATORY ANTI-PATTERNS: ...
```
