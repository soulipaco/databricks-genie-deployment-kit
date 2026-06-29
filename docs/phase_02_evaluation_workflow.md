# Phase 02 — Evaluation Workflow

Use this workflow for ongoing benchmark evaluation and quality improvement.

## Cadence

Run after every significant change to:
- `instructions/general.md`
- Active example_sql files
- Active filter or measure snippets
- Table schemas or column metadata

## Workflow

### Step 1: Materialize and Validate
```bash
python scripts/materialize.py
python scripts/validate.py          # Must return 0 errors
```

### Step 2: Deploy
```bash
python scripts/push_folder_to_room.py
```

### Step 3: Prepare Evaluation Batch
```bash
python scripts/prepare_eval.py --output build/eval_batch.yml
```

### Step 4: Run Evaluation
- Submit each benchmark question to the live Genie room
- Record model SQL output and semantic pass/fail
- Store results in `build/eval_<date>.yml`

### Step 5: Analyze Failures
- Run skill: `analyze_benchmark_failures`
- Follow `geniecode/BENCHMARK_UPDATE_PROCEDURES.md` 10-step flowchart

### Step 6: Apply Fixes
- Apply P0 fixes first (systemic general.md rules)
- Then P1 (missing example_sql)
- Then P2 (snippet fixes)
- Then P3 (individual benchmark fixes)

### Step 7: Validate Fixes
```bash
python scripts/validate.py
```

### Step 8: Log Results
- Add session to `docs/11_failed_evaluation_tracking.md`
- Add new patterns to `geniecode/FIX_PATTERNS.md`
- Update `geniecode/KNOWLEDGE_BASE.md` asset counts

### Step 9: Re-evaluate Previously Failed Benchmarks
Confirm that fixes resolved the failures before closing the session.
