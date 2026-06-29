# Phase 01 — Authoring Workflow (New Room)

Use this workflow to author all assets for a new Genie room from scratch.

## Prerequisites
- Room configured (`room.config.yml` populated)
- At least one table registered (`data_sources/tables.yml`)
- Column metadata files created

## Workflow

### Step 1: General Instructions
1. Read all `metadata/columns/<table>.yml` files
2. Read `geniecode/DOMAIN_RULES.md` for room-wide conventions
3. Draft `instructions/general.md` following `docs/18_general_instruction_production_workflow.md`

### Step 2: Generate Measures
1. Run skill: `generate_measures`
2. Activate high-priority measures
3. Run `python scripts/materialize.py`

### Step 3: Generate Filters
1. Run skill: `generate_filters`
2. Activate dimension + temporal filters
3. Run `python scripts/materialize.py`

### Step 4: Generate Example SQL
1. Use question taxonomy for coverage planning
2. Run skill: `generate_example_sql` for each category
3. Check capacity after each batch
4. Run `python scripts/materialize.py`

### Step 5: Generate Benchmarks
1. Run skill: `generate_benchmarks`
2. Cover all question taxonomy categories
3. Aim for 20+ benchmarks minimum

### Step 6: Validate and Deploy
1. `python scripts/validate.py`
2. `python scripts/push_folder_to_room.py`
3. Test in live room

### Step 7: Evaluate and Iterate
1. Run `run_benchmark_evaluation` skill
2. Run `analyze_benchmark_failures` skill
3. Apply fixes using `geniecode/BENCHMARK_UPDATE_PROCEDURES.md`
4. Re-evaluate
