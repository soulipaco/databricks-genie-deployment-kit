# Example SQL Corpus

All example SQL entries live here. This is the full superset.
Activate an entry by adding its `id` to `instruction_library/activation/example_sql.active.yml`.

## Capacity Note
Capacity = 100 (total) - 1 (general) - N (tables) = max active example_sql.
Check before activating: `python scripts/materialize.py --check-limits`

## Required Fields
- `id` — 32-char hex
- `question` — Natural language question
- `sql` — Ground-truth SQL

## Recommended Fields
- `parameters` — If using `:StartDate` / `:EndDateExclusive`
- `usage_guidance` — TRIGGER PHRASES, DATE BINDING, anti-patterns

See `templates/example_sql.yml` for the template.
