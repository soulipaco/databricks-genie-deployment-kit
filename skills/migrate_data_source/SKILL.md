# Skill: migrate_data_source

## Trigger
- "migrate the data source"
- "switch to a new table"
- "replace the source table"
- "update the metric view"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `old_table` | User | Yes |
| `new_table` | User | Yes (3-level identifier) |
| `column_mapping` | User | No (list of old→new column name changes) |

## Steps

1. **Read current data_sources/tables.yml** — Note the old table entry.

2. **Read geniecode/TABLE_SCHEMAS.md** for the old table schema.

3. **Read all filter, measure, and example_sql files** — Find every reference to the old table identifier.

4. **Create a migration plan** — List all files that need updates.

5. **Update data_sources/tables.yml** — Replace old table entry with new one.

6. **Create new metadata/columns/<new_table>.yml** — With column configs for the new table.

7. **For each filter file referencing the old table:**
   - If the SQL references the old table by name, update it
   - Apply column_mapping if column names changed

8. **For each measure file referencing the old table:**
   - Update table references
   - Apply column_mapping

9. **For each example_sql file:**
   - Update the FROM clause and all column references
   - Apply column_mapping

10. **For each benchmark file:**
    - Update the FROM clause and all column references
    - Apply column_mapping

11. **Update instructions/general.md** — Update table name references.

12. **Update geniecode/TABLE_SCHEMAS.md** — Replace old table section.

13. **Run validation** — `python scripts/validate.py`.

14. **Run snippet health check** — `python geniecode/scripts/snippet_health_check.py --mode full`.

15. **Report migration summary** — Files changed, issues found.

## Outputs

- Updated `data_sources/tables.yml`
- New `metadata/columns/<new_table>.yml`
- Updated filter, measure, example_sql, benchmark files
- Updated `instructions/general.md`
- Updated `geniecode/TABLE_SCHEMAS.md`

## Validation

- [ ] No references to old table remain in active files
- [ ] New table has 3-level identifier
- [ ] All SQL uses new column names
- [ ] `python scripts/validate.py` returns 0 errors
- [ ] Snippet health check passes

## References

- `AGENTS.md` — Format specs for all file types
- `geniecode/TABLE_SCHEMAS.md` — Schema documentation to update
