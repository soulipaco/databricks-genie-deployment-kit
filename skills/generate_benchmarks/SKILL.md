# Skill: generate_benchmarks

## Trigger
- "generate benchmarks"
- "create benchmark questions"
- "add benchmarks for <topic>"
- "build out the benchmark set"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `question` | User | Yes |
| `ground_truth_sql` | User or generated | Yes |
| `question_category` | User | No (inferred from question) |

## Steps

1. **Read geniecode/KNOWLEDGE_BASE.md** — Understand routing, date logic, conventions.

2. **Read geniecode/TABLE_SCHEMAS.md** — Confirm table grain, date column, measures.

3. **Read existing benchmarks/** — Understand coverage and avoid near-duplicates.

4. **Classify the question** using the taxonomy in `docs/06_question_taxonomy.md`:
   - Category A: Summary / ranking by dimension
   - Category B: Trend analysis (weekly/monthly)
   - Category C: Top-N ranking
   - Category D: Comparison (period over period, entity vs average)
   - Category E: Pareto / root-cause distribution
   - Category F: Individual entity lookup
   - Category G: Parameterized date ranges
   - Category H: Complex multi-step

5. **Write the ground-truth SQL:**
   - Use 3-level fully qualified table names
   - Dynamic dates only (CURRENT_DATE expressions)
   - Half-open date boundaries
   - ILIKE for text filters
   - Filtered dimensions in SELECT
   - Only columns relevant to the question (avoid over-scoping)
   - For metric views: MEASURE() + GROUP BY ALL

6. **Generate a unique ID** and determine the next available file number.

7. **Write to `benchmarks/<NN>_<slug>.yml`**:
   ```yaml
   id: <32-char hex>
   question: <question text>
   answer_format: SQL
   sql: <ground-truth SQL>
   ```

8. **For parameterized benchmarks** — Add `:StartDate`, `:EndDateExclusive` parameters.

9. **Check for hardcoded dates** — If any exist, add `_cleanup_flags` and note as technical debt.

10. **Run validation** — `python scripts/validate.py`.

## Outputs

- New files in `benchmarks/`

## Ground-Truth SQL Rules

| Rule | Detail |
|------|--------|
| Table qualification | 3-level: `catalog.schema.table` |
| Date format | Dynamic (CURRENT_DATE expressions), never hardcoded |
| Date boundaries | Half-open: `>= start AND < end_exclusive` |
| Text filters | `ILIKE '%value%'` (never `=` for text) |
| Metric views | `MEASURE(kpi)` + `GROUP BY ALL` |
| Output columns | Only what the question asks for |
| Ordering | Descending for rankings, ascending for trends |
| Default limit | 5 for top-N questions |

## Validation

- [ ] Benchmark ID is unique (no duplicates in benchmarks/)
- [ ] No hardcoded dates (or flagged in _cleanup_flags)
- [ ] Table is 3-level qualified
- [ ] Text filters use ILIKE
- [ ] Ground truth answers the stated question exactly
- [ ] Output columns match what user would expect
- [ ] `python scripts/validate.py` returns 0 errors

## References

- `AGENTS.md` — Benchmark YAML format spec
- `geniecode/DOMAIN_RULES.md` — Date and filter rules
- `templates/benchmark.yml` — Benchmark template
- `docs/06_question_taxonomy.md` — Question classification taxonomy
- `docs/09_benchmark_question_bank.md` — Bank of question patterns to use
- `docs/07_question_generation_rules.md` — Question authoring rules
