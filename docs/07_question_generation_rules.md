# 07 — Question Generation Rules

## Universal Rules

1. **One question, one answer** — Each benchmark answers exactly one question.
2. **Natural language only** — Questions should sound like natural user input.
3. **No domain jargon in question text** (unless testing jargon recognition).
4. **Cover all categories** — Use taxonomy in `06_question_taxonomy.md`.
5. **Avoid near-duplicates** — Check existing benchmarks before adding.

## SQL Quality Rules

1. **3-level table qualification** — Always `catalog.schema.table`.
2. **Dynamic dates only** — Use CURRENT_DATE() expressions, never hardcoded.
3. **Half-open date boundaries** — `>= start AND < end_exclusive`.
4. **ILIKE for text filters** — Never `=` for text dimension values.
5. **Filtered dimensions in SELECT** — If filtering on a column, include it in output.
6. **Minimal output** — Only columns the question asks for.
7. **Correct aggregation pattern** — MEASURE() for metric views, SUM/COUNT for raw.

## Question Coverage Targets

| Category | Recommended minimum |
|----------|--------------------|
| A (Summary) | 10% of total |
| B (Trend) | 15% of total |
| C (Top-N) | 20% of total |
| D (Comparison) | 15% of total |
| E (Pareto) | 10% of total |
| F (Entity lookup) | 10% of total |
| G (Parameterized) | 10% of total |
| H (Complex) | 10% of total |
