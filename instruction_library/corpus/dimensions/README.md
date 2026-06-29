# Dimension Helpers Corpus

Dimension helpers are repo-only — they appear in `instructions/sql_snippets/dimensions/`
but are NOT deployed to the Genie room API.

They provide reusable SELECT expressions for period boundaries, grain labels, and
other structural output fields that are referenced by multiple example_sql files.

## Required Fields
- `id` — 32-char hex
- `alias` — Output column name
- `display_name` — Human-readable name
- `sql` — SELECT expression
