# 10 — Evaluation Adjustment Workflow

## Default Operating Rules

1. **Mandatory 3-way comparison** — Always compare GT SQL, model SQL, AND the active snippet SQL before concluding.
2. **Read the snippet first** — Find and read the actual active snippet (not just its filename) before analysis.
3. **Prefer fixing GT** — If the model is semantically correct but the GT has extra columns or wrong logic, fix the GT first.
4. **Prefer general.md for systemic issues** — If the same root cause affects 3+ benchmarks, fix general.md instead of adding individual examples.
5. **Tighten over add** — Before adding a new example_sql, try tightening the wrong example's `usage_guidance` first.
6. **Explicit anti-patterns** — Add "Do NOT..." rules to usage_guidance to prevent retrieval collisions.
7. **Mandatory capacity check** — Check capacity before activating any new example_sql.
8. **Update both copies** — When fixing an example_sql, update both the `instructions/example_sql/` copy AND the `instruction_library/corpus/example_sql/` copy.
9. **Validate before declaring done** — Run `python scripts/validate.py` after every fix batch.
10. **Log all fixes** — Update `docs/11_failed_evaluation_tracking.md` after each evaluation cycle.

## Root-Cause Classes

See `geniecode/BENCHMARK_WORKSPACE.md` for the complete 7-class taxonomy.

## SQL Safety Rule

Before adding any SQL to a benchmark or example_sql:
- [ ] No hardcoded dates (or flagged in `_cleanup_flags`)
- [ ] 3-level table qualification
- [ ] ILIKE for text filters
- [ ] Half-open date boundaries
- [ ] Filtered dimensions in SELECT

## Tracking Standard

After each evaluation session:
1. Record the session in `docs/11_failed_evaluation_tracking.md`
2. Add new patterns to `geniecode/FIX_PATTERNS.md`
3. Update `geniecode/KNOWLEDGE_BASE.md` asset counts
4. Update `CHANGELOG.md` with version bump if significant changes
