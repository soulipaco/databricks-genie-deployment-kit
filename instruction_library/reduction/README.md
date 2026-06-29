# Reduction — Merge and Isolation Decision Records

This directory stores analysis and decisions about snippet merges and deactivations.

## When to Add a Record

1. When CHK-1 (exact SQL duplicates) is found and snippets are merged
2. When a snippet is deliberately deactivated to reclaim capacity
3. When similarity analysis concludes a snippet is redundant

## Record Format

```
### YYYY-MM-DD — <decision title>
**Type:** MERGE / DEACTIVATE / CONSOLIDATE
**Snippets involved:** <IDs or filenames>
**Reason:** <why the decision was made>
**Outcome:** <what was kept, what was removed>
**Alternatives covered by:** <what now covers the use case>
```
