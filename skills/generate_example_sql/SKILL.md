# Skill: generate_example_sql

## Trigger
- "generate example sql"
- "generate example queries"
- "create example sql for benchmarks"
- "add example sql for <topic>"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `question` | User | Yes |
| `table_name` | User or inferred | Yes |
| `sql_pattern` | User or inferred | No (summary / trend / top-n / pareto / ...) |
| `parameters` | User | No |

## Steps

1. **Read geniecode/KNOWLEDGE_BASE.md** — Understand source routing and date logic.

2. **Read geniecode/TABLE_SCHEMAS.md** — Confirm table grain, date column, measures.

3. **Read instructions/general.md** — Understand room-wide SQL rules and conventions.

4. **Check for existing similar questions** in `instruction_library/corpus/example_sql/` — Avoid near-duplicates.

5. **Classify the question pattern:**
   - Summary: `SELECT dims, MEASURE(kpi) FROM table GROUP BY ALL`
   - Trend: add date truncation and ORDER BY date
   - Top-N: add `ORDER BY metric DESC LIMIT 5`
   - Pareto: cumulative percentage calculation
   - Parameterized: use `:StartDate`, `:EndDateExclusive`, `:PeriodGrain`

6. **Generate the SQL:**
   - Use 3-level fully qualified table names
   - Dynamic dates only (no hardcoded values)
   - Include all filtered dimensions in SELECT
   - Text filters use ILIKE
   - For metric views: use MEASURE() + GROUP BY ALL
   - For raw tables: use standard aggregations

7. **Add usage_guidance:**
   - TRIGGER PHRASES: list all question variants this example covers
   - DATE BINDING: if parameterized, provide explicit binding formulas
   - MANDATORY OUTPUT CONTRACT: list required columns
   - MANDATORY ANTI-PATTERNS: list what NOT to do (prevents retrieval collision)

8. **Generate a unique ID** and determine the next available file number.

9. **Write to `instruction_library/corpus/example_sql/<NN>_<slug>.yml`**.

10. **Ask user if this should be activated immediately** — If yes and within budget, add to `instruction_library/activation/example_sql.active.yml`.

11. **Run materialize and validate.**

## Outputs

- New file in `instruction_library/corpus/example_sql/`
- Updated `instruction_library/activation/example_sql.active.yml` (if activating)
- Updated `instructions/example_sql/` (after materialize)

## SQL Templates by Pattern

### Summary with Ranking
```sql
SELECT dimension, MEASURE(kpi) AS metric_name
FROM catalog.schema.metric_view
WHERE date_col >= :StartDate AND date_col < :EndDateExclusive
GROUP BY ALL
HAVING metric_name > 0
ORDER BY metric_name DESC
LIMIT 5
```

### Trend by Week
```sql
SELECT
  DATE_TRUNC('WEEK', date_col) AS week_start,
  MEASURE(kpi) AS metric_name
FROM catalog.schema.metric_view
WHERE date_col >= DATE_SUB(DATE_TRUNC('WEEK', CURRENT_DATE()), 84)  -- 12 weeks
  AND date_col < DATE_TRUNC('WEEK', CURRENT_DATE())
GROUP BY ALL
ORDER BY week_start
```

### Parameterized Date Range
```sql
SELECT dimension, MEASURE(kpi) AS metric_name
FROM catalog.schema.metric_view
WHERE date_col >= :StartDate AND date_col < :EndDateExclusive
GROUP BY ALL
ORDER BY metric_name DESC
```

## Validation

- [ ] ID is unique (check all existing example_sql files)
- [ ] Table name is 3-level qualified
- [ ] No hardcoded dates
- [ ] Text filters use ILIKE
- [ ] Filtered columns appear in SELECT
- [ ] `usage_guidance` has TRIGGER PHRASES to prevent retrieval collision
- [ ] Capacity not exceeded: check `instruction_library/activation/limits.yml`
- [ ] `python scripts/validate.py` returns 0 errors

## References

- `AGENTS.md` — Example SQL YAML format spec
- `geniecode/DOMAIN_RULES.md` — Date windows and filter rules
- `templates/example_sql.yml` — Example SQL template
- `docs/07_question_generation_rules.md` — Question authoring rules
- `docs/08_asset_generation_playbook.md` — Playbook for generating assets systematically
