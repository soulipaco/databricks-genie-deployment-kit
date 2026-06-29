# 17 — Measure Migration Policy

## When to Migrate a Measure

Same triggers as filter migration (see `15_filter_migration_policy.md`).

## Migration Steps

1. **Copy the measure file** from `instructions/sql_snippets/measures/` to `instruction_library/corpus/measures/`.
2. **Preserve the `id` field** exactly.
3. **Add to activation manifest** — Add the ID to `instruction_library/activation/measures.active.yml`.
4. **Run materialize** — `python scripts/materialize.py`.
5. **Validate** — `python scripts/validate.py`.

## Measure-Specific Checks

- [ ] `alias` field is set (output column name)
- [ ] SQL uses MEASURE() if the source is a metric view
- [ ] `instruction` field documents grain restrictions
- [ ] No duplicate alias across all active measures
