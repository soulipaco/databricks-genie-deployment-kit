# Skill: generate_measures

## Trigger
- "generate measures"
- "generate measure snippets"
- "create measure snippets from column metadata"
- "add measures for <table>"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `table_name` | User or inferred from context | Yes |
| `columns` | Read from `metadata/columns/<table>.yml` | Yes |
| `existing_measures` | Read from `instruction_library/corpus/measures/` | Auto |

## Steps

1. **Read metadata/columns/<table>.yml** — Identify columns that are numeric KPIs or semantic measures.

2. **Read instruction_library/corpus/measures/** — Identify existing measures to avoid duplicates.

3. **Read instructions/general.md** — Understand KPI rules (MEASURE() vs raw, grain constraints).

4. **Read geniecode/TABLE_SCHEMAS.md** — Understand which columns support MEASURE() and which are raw aggregations.

5. **For each measure to generate:**
   - Generate a unique ID: `python -c "import uuid; print(uuid.uuid4().hex)"`
   - Determine the SQL expression:
     - If the column is a semantic measure: `MEASURE(<column_name>)`
     - If the column is a raw count: `COUNT(DISTINCT <id_column>)`
     - If the column is a sum: `SUM(<column_name>)`
     - If the column is a ratio: `SUM(<numerator>) / NULLIF(SUM(<denominator>), 0)`
   - Set `alias` to a descriptive snake_case name
   - Set `display_name` to a human-readable title
   - Write `instruction` with WHEN_TO_USE, SCOPE_TABLES, RISK_IF_MISUSED

6. **Determine sequential file number** — Check existing files in `instruction_library/corpus/measures/` and use the next available number.

7. **Write each measure to `instruction_library/corpus/measures/<NN>_<slug>.yml`**.

8. **Ask user which measures should be immediately activated** — Add approved IDs to `instruction_library/activation/measures.active.yml`.

9. **Run materialize** — `python scripts/materialize.py`.

10. **Run validation** — `python scripts/validate.py`.

## Outputs

- New files in `instruction_library/corpus/measures/`
- Updated `instruction_library/activation/measures.active.yml` (if activating)
- Updated `instructions/sql_snippets/measures/` (after materialize)

## MEASURE() vs Raw Aggregation Rules

| When | Use |
|------|-----|
| Table is a metric view with pre-computed KPIs | `MEASURE(<column>)` |
| Table is a raw events table with numeric columns | `SUM()` or `COUNT()` |
| Column is a ratio/rate KPI | `MEASURE(<column>)` — NOT manual division |
| Need percentage output | `CONCAT(ROUND(MEASURE(<col>) * 100, 2), '%')` |

## Validation

- [ ] All measure IDs are unique (no duplicates with existing measures)
- [ ] Measure SQL uses correct pattern for the table type (MEASURE() vs raw)
- [ ] Each measure has a `display_name` and `alias`
- [ ] `instruction` field documents WHEN_TO_USE and SCOPE_TABLES
- [ ] `python scripts/validate.py` returns 0 errors

## References

- `AGENTS.md` — Measure YAML format spec
- `geniecode/TABLE_SCHEMAS.md` — Which columns use MEASURE()
- `geniecode/DOMAIN_RULES.md` — KPI aggregation rules
- `templates/measure_simple.yml` — Simple measure template
- `templates/measure_ratio.yml` — Ratio measure template
- `docs/16_measure_instruction_skeleton.md` — Instruction authoring guide
