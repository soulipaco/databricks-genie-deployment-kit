# Skill: add_data_source

## Trigger
- "add a table"
- "add a data source"
- "register a new table"
- "add a new metric view"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `table_identifier` | User | Yes (`catalog.schema.table_name`) |
| `table_description` | User | Yes |
| `key_columns` | User | Yes (list of important column names) |
| `exclude_columns` | User | No (columns to hide from Genie) |
| `entity_match_columns` | User | No (columns for fuzzy entity matching) |

## Steps

1. **Read data_sources/tables.yml** — Check if the table already exists.

2. **Validate the table identifier** — Must be 3-level: `catalog.schema.table`.
   - If only 1-2 levels given: ask user for the full identifier.

3. **Add to data_sources/tables.yml**:
   ```yaml
   - identifier: catalog.schema.table_name
     description: <table_description>
     column_metadata_file: metadata/columns/table_name.yml
   ```

4. **Create metadata/columns/<table_name>.yml**:
   ```yaml
   table: catalog.schema.table_name
   columns:
     - column_name: <key_column>
       enable_entity_matching: true
     - column_name: <exclude_column>
       exclude: true
   ```

5. **Update instructions/general.md** — Add a section for the new table:
   - Grain description
   - Date column name
   - Key dimension columns
   - Any special aggregation rules

6. **Update geniecode/TABLE_SCHEMAS.md** — Add a new section for this table following the template.

7. **Update geniecode/KNOWLEDGE_BASE.md** — Update the source routing table and question routing heuristic.

8. **Run validation** — `python scripts/validate.py`.

## Outputs

- Updated `data_sources/tables.yml`
- New `metadata/columns/<table_name>.yml`
- Updated `instructions/general.md`
- Updated `geniecode/TABLE_SCHEMAS.md`
- Updated `geniecode/KNOWLEDGE_BASE.md`

## Validation

- [ ] Table identifier is 3-level (`catalog.schema.table`)
- [ ] `metadata/columns/<table>.yml` exists for every table in `data_sources/tables.yml`
- [ ] `instructions/general.md` documents the new table's grain and date column
- [ ] `python scripts/validate.py` returns 0 errors

## References

- `AGENTS.md` — `data_sources/tables.yml` and column metadata format specs
- `geniecode/TABLE_SCHEMAS.md` — Schema reference to update
- `geniecode/KNOWLEDGE_BASE.md` — Source routing table to update
- `docs/01_room_asset_map.md` — Asset map documentation
