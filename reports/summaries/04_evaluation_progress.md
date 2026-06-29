# Evaluation Progress — {{ROOM_TITLE}}

> **Report date:** {{REPORT_DATE}} | {{EVAL_SESSION_COUNT}} evaluation session(s)

## Summary

| Metric | Value |
|--------|-------|
| Total Sessions | {{EVAL_SESSION_COUNT}} |
| Total Evaluated | {{TOTAL_EVALUATED}} |
| Passed | {{TOTAL_PASSED}} |
| Failed | {{TOTAL_FAILED}} |
| Overall Pass Rate | {{PASS_RATE}} |

## Failure Mode Distribution

| Class | Description | Count |
|-------|-------------|-------|
| 1 — OUTPUT-SHAPE | Correct logic, wrong output format | {{CLASS_1_COUNT}} |
| 2 — SEMANTIC-GENERATION | Wrong logic/table/metric | {{CLASS_2_COUNT}} |
| 3 — BENCHMARK-DEFECT | Ground truth was wrong | {{CLASS_3_COUNT}} |
| 4 — EVALUATOR-FRAGILITY | False negative from evaluator | {{CLASS_4_COUNT}} |
| 5 — MIXED | Both GT and model have issues | {{CLASS_5_COUNT}} |
| 6 — RETRIEVAL-COLLISION | Wrong similar example retrieved | {{CLASS_6_COUNT}} |
| 7 — SNIPPET-CONTRADICTION | Snippet guidance contradicts itself | {{CLASS_7_COUNT}} |

## Session History

*Run `python reports/scripts/generate_inventory.py` to auto-populate from `build/eval_*.yml`.*

{{SESSION_HISTORY}}
