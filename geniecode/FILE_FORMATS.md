# File Formats Reference — {{ROOM_NAME}}
> **Last updated:** {{UPDATE_DATE}}
> YAML/MD format specs for every asset type in the deployment kit.

---

## Benchmark YAML (`benchmarks/<NN>_<slug>.yml`)
```yaml
id: <32-char hex>                    # Generate: python -c "import uuid; print(uuid.uuid4().hex)"
question: <natural language question>
answer_format: SQL
sql: <ground-truth SQL string>
_cleanup_flags: [...]                # Optional - known issues like hard-coded dates
```

## Example SQL YAML (`instructions/example_sql/<NN>_<slug>.yml`)
```yaml
id: <32-char hex>
question: <natural language question>
sql: <SQL query string>
parameters:                          # Optional
  - name: StartDate
    type_hint: DATE
  - name: EndDateExclusive
    type_hint: DATE
  - name: PeriodMode
    type_hint: INTEGER               # 0=WEEK, 1=MONTH, 2=DAY
usage_guidance: |                    # Optional - when/how Genie should use this
  Use for ...
  TRIGGER PHRASES: ...
  DATE BINDING: StartDate = ..., EndDateExclusive = ...
  MANDATORY OUTPUT CONTRACT: <list required columns>
  MANDATORY ANTI-PATTERNS: Do NOT ...
_cleanup_flags: ['2025-03-01']       # Optional - hard-coded dates to fix
```

## Filter Snippet YAML (`instructions/sql_snippets/filters/<NN>_<slug>.yml`)
```yaml
id: <32-char hex>
display_name: <human-readable name>
sql: <WHERE clause fragment - NO 'WHERE' keyword, just conditions>
synonyms: [alias1, alias2]           # Optional - alternative names
instruction: |                       # Optional
  WHEN_TO_USE: Apply when user filters by <dimension>.
  SCOPE_TABLES: <table_name>.
  TIMEFRAME_HINT: <applicable time range, or 'any'>.
  RISK_IF_MISUSED: <what goes wrong if applied incorrectly>.
```

## Measure Snippet YAML (`instructions/sql_snippets/measures/<NN>_<slug>.yml`)
```yaml
id: <32-char hex>
alias: <column alias>                # Output column name
display_name: <human-readable name>
sql: <SELECT expression - aggregation formula>
synonyms: [alias1, alias2]           # Optional
instruction: |                       # Optional
  WHEN_TO_USE: Use to calculate <metric>.
  SCOPE_TABLES: <table_name>.
  RISK_IF_MISUSED: <what goes wrong>.
```

## Dimension Helper YAML (`instructions/sql_snippets/dimensions/<NN>_<slug>.yml`)
```yaml
id: <32-char hex>
alias: <column alias>
display_name: <human-readable name>
sql: <SELECT expression for reusable output field>
instruction: <when to use, scope, risks>  # Optional
```

`instructions/dimensions/` is a repo-only helper layer. It is NOT part of the current room deploy payload.

## Column Metadata YAML (`metadata/columns/<table>.yml`)
```yaml
table: catalog.schema.table_name
columns:
  - column_name: <name>
    exclude: true                    # Hide from Genie (optional)
    enable_format_assistance: true   # Help with formatting (optional)
    enable_entity_matching: true     # Enable fuzzy matching (optional)
    get_example_values: true         # Fetch sample values (optional)
    build_value_dictionary: true     # Build value lookup (optional)
```

## Room Config (`room.config.yml`)
```yaml
room_name: <identifier>
title: <display title>
description: <markdown description>
version: 2
purpose: <note>
source_of_truth: repo
parent_path: <workspace path>
sample_questions:
  - id: <32-char hex>
    question: <text>
data_sources: data_sources/tables.yml
column_metadata: metadata/columns/
instructions:
  general: instructions/general.md
  example_sql: instructions/example_sql/
  sql_snippets:
    filters: instructions/sql_snippets/filters/
    measures: instructions/sql_snippets/measures/
benchmarks: benchmarks/
bootstrap_snapshot: snapshots/exported_space.json
```

## Environment Config (`env/<name>.yml`)
```yaml
environment: <name>                  # local, staging, prod
workspace_url: https://<host>
warehouse_id: <SQL warehouse ID>
space_id: <Genie space ID or null for new>
parent_path: <workspace folder path>
```

## Activation Manifest (`instruction_library/activation/<type>.active.yml`)
```yaml
asset_type: <filters|measures|dimensions|example_sql>
active_ids:
  - <32-char hex>   # 01_snippet_name.yml
  - <32-char hex>   # 02_snippet_name.yml
```

## Capacity Limits (`instruction_library/activation/limits.yml`)
```yaml
max_total_space_instructions: 100
general_text_instruction_count: 1
table_description_count_mode: auto_from_data_sources_tables
active_budgets:
  example_sql:
    mode: derived_total_minus_general_minus_tables
  filters:
    max_active: 100
  measures:
    max_active: 100
```

## General Instructions (`instructions/general.md`)
```markdown
# General Instructions

> **Source ID:** `<id>`
> Edit this file as the source of truth.

---

<Free-text rules for the Genie LLM: grain logic, KPI rules,
aggregation conventions, date handling, formatting rules, etc.>
```

## ID Generation
```python
import uuid
new_id = uuid.uuid4().hex  # 32-char hex string
```

## File Naming Convention
- Numbered prefix: `01_`, `02_`, ... (sequential)
- Followed by slug of the question/name
- Extension: `.yml`
- Example: `42_total_revenue_by_region_last_month.yml`

## Safety Rules
- Never duplicate IDs across any asset type
- Never edit `snapshots/` or `build/`
- Never hard-code dates in SQL
- Never point deploy at `instruction_library/` directly (always through `instructions/`)
- Preserve `_cleanup_flags` until the underlying issue is fixed
- Always run `python scripts/validate.py` after changes
