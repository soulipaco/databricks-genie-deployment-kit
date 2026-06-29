# 03 — Placeholder vs Real Content Policy

## What is a Placeholder?

A `{{PLACEHOLDER}}` is a token in a template file that must be replaced with
a real value before the file can be used. Placeholders use the syntax `{{NAME}}`.

## Rules

### Templates (ok to have placeholders)
- `room.config.yml` — The room config template
- `templates/*.yml` — All asset templates
- `env/local.yml`, `env/prod.yml` — Env configs before personalization
- `geniecode/*.md` — Knowledge base stubs before domain configuration

### Production Files (must NOT have placeholders)
- `instructions/general.md` — No placeholders in deployed general instruction
- `instructions/example_sql/*.yml` — No placeholders in deployed SQL
- `instructions/sql_snippets/**/*.yml` — No placeholders in active snippets
- `benchmarks/*.yml` — No placeholders in ground truth SQL
- `data_sources/tables.yml` — No placeholders in table identifiers

### How to Replace Placeholders

1. `{{32_CHAR_HEX_ID}}` → Run: `python -c "import uuid; print(uuid.uuid4().hex)"`
2. `{{ROOM_NAME}}` → Short identifier, no spaces (e.g., `analytics_room_v1`)
3. `{{CATALOG}}.{{SCHEMA}}.{{TABLE}}` → Full 3-level table identifier
4. `{{WORKSPACE_PARENT_PATH}}` → Workspace folder path (e.g., `/Users/user@company.com`)
