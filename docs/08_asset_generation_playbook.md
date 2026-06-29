# 08 — Asset Generation Playbook

## Phase 1: Table Discovery
1. Read `data_sources/tables.yml` — List all registered tables
2. Read `metadata/columns/<table>.yml` for each — Identify KPI columns, dimension columns, date columns
3. Read `geniecode/TABLE_SCHEMAS.md` — Understand grain, date column, LOB column
4. Read `instructions/general.md` — Understand room-wide conventions

## Phase 2: Measure Generation
1. List all numeric KPI columns in each table
2. For metric views: map each to `MEASURE(<column>)` pattern
3. For raw tables: determine correct aggregation (SUM, COUNT DISTINCT, ratio)
4. Generate using `skills/generate_measures/SKILL.md`
5. Target: all KPI columns covered by at least one measure snippet

## Phase 3: Filter Generation
1. List all dimension columns eligible for filtering
2. Generate dimension filters (text → ILIKE, categorical → =)
3. Generate temporal filters (yesterday, last week, last month, last N months, this month)
4. Generate any domain-specific filters (exclusions, scope restrictions)
5. Generate using `skills/generate_filters/SKILL.md`

## Phase 4: Example SQL Generation
1. Use question taxonomy (`06_question_taxonomy.md`) to ensure category coverage
2. Generate at least 2-3 examples per category
3. Prioritize parameterized examples (`:StartDate`, `:EndDateExclusive`) for temporal flexibility
4. Generate using `skills/generate_example_sql/SKILL.md`
5. Check capacity before activating

## Phase 5: Benchmark Generation
1. For each example SQL, create a corresponding benchmark
2. Ensure GT SQL is correct and minimal (no extra columns)
3. Add at least 2 benchmarks per category
4. Generate using `skills/generate_benchmarks/SKILL.md`

## Phase 6: Validation and Deploy
1. `python scripts/materialize.py`
2. `python scripts/validate.py` — Must return 0 errors
3. `python scripts/push_folder_to_room.py`
4. Test in the live room with sample questions
