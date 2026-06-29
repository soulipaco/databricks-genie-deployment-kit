# 15 — Filter Migration Policy

## When to Migrate a Filter

Migrate a filter (move from `instructions/` directly to `instruction_library/corpus/`) when:
- The filter was pulled from the live room via `pull_room_to_folder.py`
- The filter needs to be edited or updated
- You want to track it in the activation manifest system

## Migration Steps

1. **Copy the filter file** from `instructions/sql_snippets/filters/` to `instruction_library/corpus/filters/`.
2. **Preserve the `id` field** exactly — do not regenerate.
3. **Add to activation manifest** — Add the ID to `instruction_library/activation/filters.active.yml`.
4. **Run materialize** — `python scripts/materialize.py` — The file will now be managed by the corpus.
5. **Validate** — `python scripts/validate.py`.

## Migration Checklist

- [ ] ID preserved
- [ ] File copied to corpus
- [ ] ID in activation manifest
- [ ] SQL follows conventions (ILIKE, half-open dates, no WHERE keyword)
- [ ] `instruction` field has WHEN_TO_USE, SCOPE_TABLES, TIMEFRAME_HINT, RISK_IF_MISUSED
- [ ] `python scripts/validate.py` returns 0 errors
