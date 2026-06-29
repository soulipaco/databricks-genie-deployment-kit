# Skill: configure_new_room

## Trigger
- "set up a new room"
- "configure a new genie room"
- "bootstrap a new room"
- "initialize this kit for a new room"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `room_name` | User | Yes |
| `room_title` | User | Yes |
| `room_description` | User | Yes |
| `parent_path` | User | Yes |
| `workspace_url` | User | Yes |
| `warehouse_id` | User | Yes |
| `table_identifiers` | User | Yes (list of `catalog.schema.table`) |
| `space_id` | User | No (null for new room) |

## Steps

1. **Read room.config.yml** — Verify the template structure.

2. **Create room.config.yml** — Replace all `{{PLACEHOLDER}}` values:
   ```yaml
   room_name: <room_name>
   title: <room_title>
   description: |-
     <room_description>
   version: 2
   source_of_truth: repo
   parent_path: <parent_path>
   ```

3. **Generate sample question IDs** — For each of 5 sample questions, generate a 32-char hex ID:
   ```python
   import uuid
   id = uuid.uuid4().hex
   ```

4. **Create env/local.yml** — Fill in workspace_url, warehouse_id, space_id (null if new).

5. **Create data_sources/tables.yml** — Add one entry per table:
   ```yaml
   tables:
     - identifier: catalog.schema.table_name
       description: <table description>
       column_metadata_file: metadata/columns/table_name.yml
   ```

6. **Create metadata/columns/<table>.yml** — For each table, create the column metadata file:
   ```yaml
   table: catalog.schema.table_name
   columns:
     - column_name: id
       exclude: false
   ```

7. **Create directory structure** — Ensure all directories exist:
   - `instructions/general.md` (stub with room name)
   - `instructions/example_sql/` (empty)
   - `instructions/sql_snippets/filters/` (empty)
   - `instructions/sql_snippets/measures/` (empty)
   - `benchmarks/` (empty)
   - `instruction_library/corpus/example_sql/` (empty)
   - `instruction_library/corpus/filters/` (empty)
   - `instruction_library/corpus/measures/` (empty)
   - `instruction_library/activation/` (with limits.yml)
   - `snapshots/` (empty)
   - `build/` (empty)

8. **Create instruction_library/activation/limits.yml**:
   ```yaml
   max_total_space_instructions: 100
   general_text_instruction_count: 1
   table_description_count_mode: auto_from_data_sources_tables
   active_budgets:
     example_sql:
       mode: derived_total_minus_general_minus_tables
     filters:
       max_active: 100
     measures:
       max_active: 100
   ```

9. **Create activation manifests** — Create empty manifests for each type:
   ```yaml
   asset_type: filters
   active_ids: []
   ```

10. **Run validation** — `python scripts/validate.py` — Confirm 0 errors.

11. **Report to user** — Summarize what was created and list the next steps:
    - Add column metadata for each table (see skill: add_data_source)
    - Generate measures and filters (see skills: generate_measures, generate_filters)
    - Generate example SQL (see skill: generate_example_sql)
    - Generate benchmarks (see skill: generate_benchmarks)

## Outputs

- `room.config.yml` — Populated room configuration
- `env/local.yml` — Local environment config
- `data_sources/tables.yml` — Table references
- `metadata/columns/<table>.yml` — Per-table column metadata stubs
- `instructions/general.md` — General instruction stub
- `instruction_library/activation/limits.yml` — Capacity limits
- `instruction_library/activation/*.active.yml` — Empty activation manifests

## Validation

- [ ] `room.config.yml` contains no `{{PLACEHOLDER}}` values
- [ ] `env/local.yml` has workspace_url, warehouse_id (space_id can be null for new rooms)
- [ ] `data_sources/tables.yml` has at least 1 table with 3-level identifier
- [ ] Each table in tables.yml has a matching `metadata/columns/*.yml` file
- [ ] `python scripts/validate.py` returns 0 errors

## References

- `AGENTS.md` — Kit structure and file format reference
- `room.config.yml` — Template to copy from
- `templates/room.config.tpl` — Full annotated room config template
- `docs/03_placeholder_vs_real_content.md` — Placeholder conventions
