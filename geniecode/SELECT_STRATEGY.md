# Select Strategy — {{ROOM_NAME}}
> Decision guide for choosing the right table and snippet for each question type.

---

## Step 1: Identify the Domain

Read the question for keywords that map to a domain:

| If question contains... | Route to... |
|------------------------|---------|
| {{KEYWORD_1}}, {{KEYWORD_2}} | {{DOMAIN_1}} → `{{TABLE_1}}` |
| {{KEYWORD_3}}, {{KEYWORD_4}} | {{DOMAIN_2}} → `{{TABLE_2}}` |

## Step 2: Identify the Pattern

| Question pattern | SQL strategy |
|-----------------|-------------|
| Summary / ranking | `SELECT dim, MEASURE(kpi) ... GROUP BY ALL HAVING MEASURE(kpi) > 0` |
| Trend over time | `SELECT period, MEASURE(kpi) ... GROUP BY ALL ORDER BY period` |
| Top N | Add `ORDER BY metric DESC LIMIT 5` |
| Comparison | Use multiple CTEs or conditional aggregation |
| Pareto | Use raw table, sum and rank by category |
| Leave-one-out | CTE with and without target entity |

## Step 3: Check for Active Example SQL

1. Search `instructions/example_sql/` for a question pattern that closely matches.
2. If found: adapt the example's SQL to the specific question.
3. If not found: search `instruction_library/corpus/example_sql/` for an inactive candidate.
4. If none: generate from scratch using domain rules.

## Step 4: Apply Snippets

1. Check `instructions/sql_snippets/filters/` for applicable filters.
2. Check `instructions/sql_snippets/measures/` for applicable measures.
3. Apply ILIKE for all text-based dimension filters.
4. Include all filtered dimensions in SELECT.
