# Fix Patterns — {{ROOM_NAME}}
> **Last updated:** {{UPDATE_DATE}}
> Living document tracking known failure patterns and their proven fixes.
> Append new patterns after each benchmark evaluation cycle.

---

## How to Use
- When analyzing a benchmark failure, check this file FIRST for known patterns.
- If the pattern matches, apply the documented fix.
- If it is a new pattern, add it after fixing.

---

## Known Patterns

### Pattern 001: Wrong date column for a specific table
- **Category:** B1
- **Symptom:** Model uses the wrong date/timestamp column (e.g., `date` instead of `created_at`)
- **Affected table:** {{TABLE_WITH_UNUSUAL_DATE_COL}}
- **Fix:** Reinforce in `general.md` which date column to use per table. Add to DOMAIN_RULES.md.
- **Example benchmarks:** (populate after first evaluation cycle)
- **Date added:** {{DATE}}

### Pattern 002: Calendar month vs rolling N days
- **Category:** B2
- **Symptom:** Model uses `DATE_SUB(CURRENT_DATE(), 30)` instead of calendar month boundaries
- **Fix:** Add explicit calendar month rule to `general.md` date section.
  - last month: `>= DATE_TRUNC('MONTH', ADD_MONTHS(CURRENT_DATE(), -1)) AND < DATE_TRUNC('MONTH', CURRENT_DATE())`
  - this month: `>= DATE_TRUNC('MONTH', CURRENT_DATE()) AND < CURRENT_DATE()`
  - last N months including current: `>= ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), -(N-1)) AND < ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), 1)`
- **Example benchmarks:** (populate after first evaluation cycle)
- **Date added:** {{DATE}}

### Pattern 003: Default LIMIT missing for top-N questions
- **Category:** H4
- **Symptom:** Model returns all results when question says "top", "highest", "lowest", "best", or "worst" without specifying N
- **Fix:** Add explicit LIMIT rule to `general.md`: "top / bottom / highest / lowest / best / worst → default LIMIT 5"
- **Example benchmarks:** (populate after first evaluation cycle)
- **Date added:** {{DATE}}

### Pattern 004: Retrieval collision between similar example SQL files
- **Category:** H1 (Retrieval Collision)
- **Symptom:** Model output closely matches a DIFFERENT active example_sql than intended
- **Root cause:** Semantically similar example_sql pulled model off-target during retrieval
- **Fix:** (1) Tighten the wrong example's `usage_guidance` with "DO NOT use for..." exclusion text. (2) Optionally activate the correct example if budget allows.
- **Example benchmarks:** (populate after first evaluation cycle)
- **Date added:** {{DATE}}

### Pattern 005: Missing ILIKE for text dimension filters
- **Category:** F1
- **Symptom:** Model uses `= 'value'` instead of `ILIKE '%value%'` for text dimension filters
- **Fix:** Reinforce in `general.md`: "All text-based dimension filters MUST use `ILIKE '%value%'`"
- **Example benchmarks:** (populate after first evaluation cycle)
- **Date added:** {{DATE}}

### Pattern 006: Snippet guidance contradicts itself (retrieval confusion)
- **Category:** H2 (Snippet Contradiction)
- **Symptom:** Model output shows "compromise" behavior (wrong ORDER BY, invented columns, wrong LIMIT) instead of following the snippet cleanly. Model deviates from snippet template.
- **Root cause:** Two lines in the snippet's `usage_guidance` give opposite instructions for the same aspect (e.g., conflicting ORDER BY priority).
- **Fix:** Remove the contradictory line. Add explicit anti-pattern: "Do NOT [wrong behavior]."
  Update BOTH `instructions/example_sql/<file>` AND `instruction_library/corpus/example_sql/<file>`.
- **Principle:** When a snippet covers multiple question variants, each variant's directive must be unambiguous. If two sort orders are needed for different variants, scope them explicitly.
- **Example benchmarks:** (populate after first evaluation cycle)
- **Date added:** {{DATE}}

### Pattern 007: Parameterized snippet missing date binding formula
- **Category:** B2 / SEMANTIC-GENERATION
- **Symptom:** Model binds date parameters incorrectly, shifting the time window by 1 month/week
- **Root cause:** Snippet had no explicit date binding formulas — model fell back to its own interpretation
- **Fix:** Add explicit date binding formulas to snippet `usage_guidance`:
  - StartDate = `ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), -(N-1))`
  - EndDateExclusive = `ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE()), 1)`
  - Anti-pattern: "Do NOT exclude the current month."
- **Principle:** Every parameterized snippet MUST include explicit date binding formulas. Never rely on general.md alone.
- **Example benchmarks:** (populate after first evaluation cycle)
- **Date added:** {{DATE}}

### Pattern 008: Model bypasses complex snippet for simplified version
- **Category:** SEMANTIC-GENERATION (Class 2)
- **Symptom:** Model generates a simplified query from scratch instead of using the complex active example_sql
- **Root cause:** Complex snippet lacked forceful anti-patterns preventing simpler alternatives
- **Fix:** Add MANDATORY ANTI-PATTERNS to the snippet: "Do NOT use simple GROUP BY — MUST use [complex pattern]."
  Add trigger phrases listing all question variants that should use this snippet.
- **Principle:** Complex statistical patterns require explicit anti-patterns forbidding simpler alternatives.
- **Example benchmarks:** (populate after first evaluation cycle)
- **Date added:** {{DATE}}

---

## Pattern Template (copy for new entries)

```
### Pattern NNN: <short description>
- **Category:** <taxonomy code>
- **Symptom:** <what the model output looks like>
- **Affected table(s):** <table name(s)>
- **Root cause:** <why the model went wrong>
- **Fix:** <what was changed and where>
- **Files changed:** <list of files>
- **Example benchmarks:** <benchmark IDs>
- **Principle:** <general rule this pattern teaches>
- **Date added:** <YYYY-MM-DD>
```

---

## Failure Category Reference

| Code | Name | Common Cause | Primary Fix |
|------|------|-------------|-------------|
| A | Wrong Source Table | Routing instructions weak | general.md routing |
| B1 | Wrong Date Column | Table-specific column not documented | general.md or filter |
| B2 | Calendar vs Rolling Days | Date formula ambiguous | general.md date rules |
| B3 | Wrong Boundaries | Inclusive vs exclusive unclear | general.md or filter |
| B4 | Missing DATE_TRUNC | Period grouping missing | example_sql |
| B5 | Wrong Default Window | Default trend not specified | general.md |
| C1 | Raw When MEASURE Needed | Table selection wrong | general.md |
| C2 | MEASURE When Raw Needed | Pareto/impact needs base table | general.md + example_sql |
| D1 | Wrong LOB Column | LOB column varies by table | general.md |
| D2 | Wrong Identity Column | Missing primary identity key | general.md |
| D4 | Missing Output Columns | Filtered dims not in SELECT | general.md |
| D5 | GT Over-Scoped | GT has unnecessary columns | benchmark |
| E1 | Averaged Interval KPI | Should sum numerators first | general.md + example_sql |
| E2 | Ranking Inversion | top/bottom vs best/worst | general.md |
| F1 | Missing ILIKE | = instead of ILIKE | general.md |
| H1 | Retrieval Collision | Similar snippet retrieved | tighten usage_guidance |
| H2 | Snippet Contradiction | Guidance contradicts itself | fix usage_guidance |
| H4 | Missing LIMIT | No top-N limit | general.md + example_sql |
| I | Correct but Different | Semantically equivalent | no fix needed |
