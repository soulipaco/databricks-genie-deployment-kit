# Skill: analyze_benchmark_failures

## Trigger
- "analyze failures"
- "triage benchmark failures"
- "analyze evaluation results"
- "classify the failures"
- "what is failing and why"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `failures` | User provides or from `build/eval_<date>.yml` | Yes |

## Steps

1. **Read geniecode/BENCHMARK_WORKSPACE.md** — Load the 7-class failure taxonomy and fix priority matrix.

2. **Read geniecode/FIX_PATTERNS.md** — Check if any failure matches a known pattern.

3. **Read geniecode/BENCHMARK_UPDATE_PROCEDURES.md** — Load the 10-step decision flowchart.

4. **For each failure, execute the mandatory 3-way comparison (STEP 3 of the flowchart):**
   a. Find and READ the closest active snippet in `instructions/example_sql/` (MANDATORY — do not skip)
   b. Compare: benchmark GT SQL vs model output SQL vs active snippet SQL
   c. Note differences in date logic, columns, aggregation, table routing, and ordering

5. **Check for snippet contradictions (STEP 4):**
   - Scan the snippet's `usage_guidance` for internal contradictions
   - Check for cross-snippet conflicts

6. **Classify each failure using the 7-class taxonomy (STEP 5):**
   - Class 1: OUTPUT-SHAPE — model logic correct, output differs
   - Class 2: SEMANTIC-GENERATION — wrong logic/table/metric
   - Class 3: BENCHMARK-DEFECT — ground truth is wrong
   - Class 4: EVALUATOR-FRAGILITY — false negative
   - Class 5: MIXED — both GT and model have issues
   - Class 6: RETRIEVAL-COLLISION — similar wrong example retrieved
   - Class 7: SNIPPET-CONTRADICTION — snippet guidance contradicts itself

7. **Group failures by root cause** — Identify batch-fixable issues.

8. **Assign priorities using the Fix Priority Matrix:**
   - P0: Shared root cause affecting 5+ benchmarks → fix general.md
   - P1: Missing example SQL for a common pattern → add example_sql
   - P2: Missing/wrong snippet → add/fix snippet
   - P3: Single-benchmark edge case → fix benchmark or targeted example
   - P4: Cosmetic difference → low priority

9. **Produce analysis report:**
   ```markdown
   ## Failure Analysis Report
   Date: <date>
   
   ### Summary
   - Total failures: N
   - Classified:
     - Class 1 (OUTPUT-SHAPE): N
     - Class 2 (SEMANTIC-GENERATION): N
     - ...
   
   ### Priority Fixes
   | P0 | Fix X in general.md — affects benchmarks: 001, 004, 018 |
   | P1 | Add example SQL for Y pattern — affects: 027, 033 |
   ...
   
   ### Recommended Fix Sequence
   1. Apply P0 fixes to general.md
   2. Add missing example SQL for P1 issues
   3. Fix individual benchmark GTs for Class 3 failures
   ```

10. **Ask user** which fixes to apply first.

## Outputs

- Structured failure analysis report
- Ranked fix recommendations by priority
- Classification of each failure

## Validation

- [ ] Every failure has a class assignment
- [ ] Every failure has a priority assignment
- [ ] P0 fixes identified (if any)
- [ ] Known patterns checked in FIX_PATTERNS.md
- [ ] 3-way comparison completed for each failure (mandatory)

## References

- `geniecode/BENCHMARK_WORKSPACE.md` — Failure taxonomy and fix priority matrix
- `geniecode/BENCHMARK_UPDATE_PROCEDURES.md` — 10-step decision flowchart
- `geniecode/FIX_PATTERNS.md` — Known patterns to check first
- `docs/10_evaluation_adjustment_workflow.md` — Evaluation workflow policy
- `docs/11_failed_evaluation_tracking.md` — Where to log failures
