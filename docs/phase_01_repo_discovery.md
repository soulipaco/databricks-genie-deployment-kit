# Phase 01 — Repo Discovery

Use this workflow to discover and map an existing room repository.

## Steps

1. **Read AGENTS.md** — Load the kit structure reference.

2. **Read geniecode/KNOWLEDGE_BASE.md** — Fast context loader.

3. **Scan root files:**
   - `room.config.yml`
   - `data_sources/tables.yml`
   - `instructions/general.md`

4. **Count assets:**
   - `benchmarks/` — count `.yml` files
   - `instructions/example_sql/` — count `.yml` files
   - `instructions/sql_snippets/filters/` — count `.yml` files
   - `instructions/sql_snippets/measures/` — count `.yml` files
   - `instruction_library/corpus/example_sql/` — count `.yml` files

5. **Read activation manifests:**
   - `instruction_library/activation/filters.active.yml`
   - `instruction_library/activation/measures.active.yml`
   - `instruction_library/activation/example_sql.active.yml`
   - `instruction_library/activation/limits.yml`

6. **Read column metadata** for each table in `data_sources/tables.yml`.

7. **Update geniecode/** — Run the self-update protocol (`geniecode/SELF_UPDATE.md`).

8. **Produce a discovery report:**
   ```
   Repository: <room_name>
   Tables: N (list identifiers)
   Benchmarks: N
   Active example_sql: N / Budget: N
   Active filters: N
   Active measures: N
   Library corpus example_sql: N
   Issues found: (list any)
   ```
