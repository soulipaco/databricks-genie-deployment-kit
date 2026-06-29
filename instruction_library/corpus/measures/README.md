# Measure Corpus

All measure snippets live here. This is the full superset.
Activate a measure by adding its `id` to `instruction_library/activation/measures.active.yml`.

## Required Fields
- `id` — 32-char hex
- `alias` — Output column name (snake_case)
- `display_name` — Human-readable name
- `sql` — SELECT expression (aggregation formula)

See `templates/measure_simple.yml` and `templates/measure_ratio.yml` for templates.
