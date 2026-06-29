# Skill: run_benchmark_evaluation

## Trigger
- "run benchmarks"
- "evaluate the room"
- "run the benchmark suite"
- "evaluate accuracy"
- "how is the room performing"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `benchmark_subset` | User | No (default: all benchmarks) |
| `env` | User | No (default: local) |

## Steps

1. **Read geniecode/BENCHMARK_WORKSPACE.md** — Understand the failure taxonomy and fix priority matrix.

2. **Read benchmarks/** — Collect all benchmark files to evaluate.

3. **Prepare evaluation batch** — Run `python scripts/prepare_eval.py --output build/eval_batch.yml`.

4. **Evaluate each benchmark against the live room:**
   For each benchmark (question, ground_truth_sql):
   a. Submit the question to the Genie room
   b. Capture the model's SQL output
   c. Compare model SQL to ground truth SQL semantically
   d. Record: Pass / Fail + reason

5. **Produce evaluation summary**:
   ```yaml
   evaluation_date: <date>
   total: N
   passed: N
   failed: N
   pass_rate: XX.X%
   failures:
     - id: <benchmark_id>
       question: <text>
       model_sql: <sql>
       gt_sql: <sql>
       reason: <why it failed>
   ```

6. **Write results to `build/eval_<date>.yml`**.

7. **Report pass rate and top failure patterns** to the user.

8. **If failures exist**, offer to:
   - Run `analyze_benchmark_failures` skill to triage
   - Apply the 10-step BENCHMARK_UPDATE_PROCEDURES.md flowchart

## Semantic Equivalence Rules

Two SQL queries are semantically equivalent if they return the same result set for any valid input:
- Same tables with same filters (different join order = equivalent)
- Same GROUP BY dimensions
- Same aggregation logic (MEASURE(x) vs direct formula = equivalent if same metric)
- Different column aliases = equivalent
- Different formatting (ROUND vs CAST) = may differ — note but do not auto-fail

## Outputs

- `build/eval_<date>.yml` — Evaluation results file
- Pass rate report
- Failure list for analysis

## Validation

- [ ] All benchmarks in `benchmarks/` are included in the evaluation
- [ ] Each failure has a reason code
- [ ] Results file written to `build/`

## References

- `geniecode/BENCHMARK_WORKSPACE.md` — Failure taxonomy
- `geniecode/BENCHMARK_UPDATE_PROCEDURES.md` — Fix procedures
- `scripts/prepare_eval.py` — Evaluation batch preparation script
- `scripts/analyze_benchmarks.py` — Results analysis script
- `docs/10_evaluation_adjustment_workflow.md` — Evaluation workflow policy
