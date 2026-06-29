# Skill: generate_filters

## Trigger
- "generate filters"
- "generate filter snippets"
- "create filter snippets from column metadata"
- "add filters for <table>"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `table_name` | User or inferred | Yes |
| `columns` | Read from `metadata/columns/<table>.yml` | Yes |
| `existing_filters` | Read from `instruction_library/corpus/filters/` | Auto |

## Steps

1. **Read metadata/columns/<table>.yml** — Identify filterable dimension columns.

2. **Read instruction_library/corpus/filters/** — Identify existing filters.

3. **Read instructions/general.md** — Understand any domain-specific filter rules.

4. **For each dimension filter to generate:**
   - Generate a unique ID
   - Determine the SQL WHERE fragment (NO `WHERE` keyword):
     - Text dimensions: `column_name ILIKE '%:FilterValue%'`
     - Categorical dimensions: `column_name = :FilterValue`
     - Boolean dimensions: `column_name = TRUE`
   - Set `display_name` to a human-readable name (e.g. "By Department")
   - Add common synonyms
   - Write `instruction` with WHEN_TO_USE, SCOPE_TABLES, TIMEFRAME_HINT, RISK_IF_MISUSED

5. **For each temporal filter to generate:**
   - Date range filters: `date_col >= :StartDate AND date_col < :EndDateExclusive`
   - Month filters: using `DATE_TRUNC('MONTH', date_col)` comparisons
   - Use half-open boundaries ALWAYS (`>= start AND < end_exclusive`)
   - NEVER use BETWEEN for date ranges

6. **Determine sequential file number** — Use next available number in `instruction_library/corpus/filters/`.

7. **Write each filter to `instruction_library/corpus/filters/<NN>_<slug>.yml`**.

8. **Ask user which filters should be activated** — Add approved IDs to `instruction_library/activation/filters.active.yml`.

9. **Run materialize** — `python scripts/materialize.py`.

10. **Run validation** — `python scripts/validate.py`.

## Outputs

- New files in `instruction_library/corpus/filters/`
- Updated `instruction_library/activation/filters.active.yml` (if activating)
- Updated `instructions/sql_snippets/filters/` (after materialize)

## Filter SQL Patterns

| Dimension type | SQL pattern |
|----------------|-------------|
| Text (free-form) | `col ILIKE '%:Value%'` |
| Category (exact) | `col = :Value` |
| Multi-value | `col IN (:Values)` |
| Date range | `col >= :StartDate AND col < :EndDateExclusive` |
| Yesterday | `col >= DATE_SUB(CURRENT_DATE(), 1) AND col < CURRENT_DATE()` |
| Last month | `col >= ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), -1) AND col < DATE_TRUNC('MONTH', CURRENT_DATE())` |
| This month | `col >= DATE_TRUNC('MONTH', CURRENT_DATE()) AND col < CURRENT_DATE()` |
| Last week | `col >= DATE_SUB(DATE_TRUNC('WEEK', CURRENT_DATE()), 7) AND col < DATE_TRUNC('WEEK', CURRENT_DATE())` |
| Last N months | `col >= ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), -(N-1)) AND col < ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), 1)` |

## Validation

- [ ] All filter IDs are unique
- [ ] Filter SQL has NO `WHERE` keyword (just the condition fragment)
- [ ] Text filters use `ILIKE '%value%'` (never `=` for text)
- [ ] Date filters use half-open boundaries (`>=` AND `<`, not BETWEEN)
- [ ] Each filter has `display_name` and `instruction` field
- [ ] `python scripts/validate.py` returns 0 errors

## References

- `AGENTS.md` — Filter YAML format spec
- `geniecode/DOMAIN_RULES.md` — Text filter and date window rules
- `templates/filter_dimension.yml` — Dimension filter template
- `templates/filter_temporal.yml` — Temporal filter template
- `docs/14_filter_instruction_skeleton.md` — Instruction authoring guide
