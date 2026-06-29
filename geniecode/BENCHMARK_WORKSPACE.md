# Benchmark Workspace — {{ROOM_NAME}}
> **Last updated:** {{UPDATE_DATE}}
> Framework for analyzing benchmark evaluation results and determining fixes.

---

## How to Use This File

When the user shares benchmark evaluations (question, model output, ground truth):

### 1. Parse the Evaluation
Extract from each row:
- **Question:** The natural language question
- **Model SQL:** What the Genie room generated
- **Ground Truth SQL:** The expected correct SQL (from benchmarks/)
- **Pass/Fail:** Whether they match semantically

### 2. Classify the Failure
For each failed benchmark, classify using the taxonomy below.

### 3. Determine Fix Location
Map each failure class to the right file(s) to modify.

### 4. Apply Fixes
Group failures by root cause and fix the shared instruction/snippet first.

---

## Failure Taxonomy (7 Classes)

### Class 1: OUTPUT-SHAPE
- Model logic correct, output format differs from GT
- **Fix:** Usually the BENCHMARK (update GT to match room conventions)

### Class 2: SEMANTIC-GENERATION
- Model used wrong metric, grain, ranking, filter logic, date logic, or business interpretation
- **Fix:** Add/update example_sql or add/clarify rule in general.md

### Class 3: BENCHMARK-DEFECT
- Ground truth does not answer the stated question, uses wrong grain/metric, or requires unnecessary output
- **Fix:** Update the BENCHMARK file (correct the GT SQL)

### Class 4: EVALUATOR-FRAGILITY
- Model SQL is semantically equivalent but evaluator flags it due to parameterization, alias naming, or shape differences
- **Fix:** Usually NONE (log as false negative). Optionally update benchmark for consistency.

### Class 5: MIXED
- Both GT and model have issues
- **Fix:** Fix BOTH — update benchmark AND fix example_sql/instruction

### Class 6: RETRIEVAL-COLLISION
- Model retrieved a similar but wrong example_sql and followed it instead of the correct one
- **Fix:** Tighten the wrong example's `usage_guidance`. Optionally activate the correct example.

### Class 7: SNIPPET-CONTRADICTION
- Active example_sql has conflicting instructions within its own `usage_guidance`, between its SQL and guidance, or with another active snippet
- **Fix:** Remove or rewrite the contradictory line. Update both active and library copies.

---

## Fix Priority Matrix

| Priority | Description | Action |
|----------|------------|--------|
| P0 | General instruction gap affecting 5+ benchmarks | Fix general.md immediately |
| P1 | Missing example_sql for a common pattern | Add example_sql to instruction_library |
| P2 | Missing/wrong snippet (filter/measure) | Add/fix snippet |
| P3 | Single benchmark with unique edge case | Fix benchmark or add targeted example_sql |
| P4 | Cosmetic difference (aliasing, formatting) | Low priority, batch later |

---

## Fix Decision Tree

```
Is the model output semantically equivalent to ground truth?
├── YES → Mark as PASS (Class 4 - evaluator fragility or Class I - correct but different)
└── NO → What is wrong?
    ├── Wrong table → Class 2 → Fix general.md routing OR add example_sql
    ├── Wrong date logic → Class 2 → Fix general.md date rules OR filter snippet
    ├── Wrong metric/grain → Class 2 → Fix general.md domain rules OR add example_sql
    ├── Wrong column/dimension → Class 2 → Fix general.md OR dimension snippet
    ├── Wrong aggregation/ranking → Class 2 → Fix general.md OR measure snippet
    ├── Wrong filter → Class 2 → Fix filter snippet OR general.md
    ├── GT wrong → Class 3 → Fix the BENCHMARK file
    ├── SQL structure wrong → Class 2 → Add example_sql for the pattern
    ├── Similar wrong example retrieved → Class 6 → Tighten wrong example guidance
    └── Snippet contradicts itself → Class 7 → Fix snippet usage_guidance
```

---

## Evaluation Session Template

```markdown
### Session: {{DATE}}
**Benchmarks evaluated:** N
**Pass:** N | **Fail:** N | **Pass rate:** X%

#### Failure Summary
| # | Benchmark | Class | Root Cause | Fix Target |
|---|-----------|-------|------------|------------|
| 1 | 042_... | B2 | Calendar month logic | general.md date rules |
| 2 | 088_... | D1 | Wrong LOB column | general.md LOB mapping |

#### Fixes Applied
| Fix | Files Modified | Benchmarks Affected |
|-----|---------------|--------------------|
| Updated calendar month rule | general.md | 042, 055, 078 |
```
