# Similarity Analysis

> When near-capacity, use this template to document similarity analysis.
> Determines which snippets can be merged, deactivated, or consolidated.

## Similarity Analysis Template

```
### Analysis: YYYY-MM-DD
**Context:** At N/M capacity for example_sql

#### Candidate Pairs for Merge/Deactivation
| Pair | Type | Similarity | Decision | Rationale |
|------|------|------------|----------|-----------|
| file_A vs file_B | CHK-1 | Exact SQL | MERGE | Identical SQL, different question text |
| file_C vs file_D | semantic | ~80% | KEEP BOTH | Cover distinct question patterns |

#### Actions Taken
- Deactivated: <IDs> → moved to isolated/deactivated.yml
- Merged: <IDs> → kept <winning_ID>
- Tightened: <IDs> → narrowed usage_guidance to prevent collision

#### Capacity After
- Active example_sql: N (was M)
- Remaining: X slots
```
