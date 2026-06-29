# Filter Corpus

All filter snippets live here. This is the full superset.
Activate a filter by adding its `id` to `instruction_library/activation/filters.active.yml`.

## File Naming
`NN_slug.yml` — Sequential number prefix + descriptive slug.

## Required Fields
- `id` — 32-char hex (generate: `python -c "import uuid; print(uuid.uuid4().hex)"`)
- `display_name` — Human-readable name
- `sql` — WHERE clause fragment (NO `WHERE` keyword)

## Optional Fields
- `synonyms` — Alternative names for entity matching
- `instruction` — Guidance with WHEN_TO_USE, SCOPE_TABLES, TIMEFRAME_HINT, RISK_IF_MISUSED

See `templates/filter_dimension.yml` and `templates/filter_temporal.yml` for templates.
