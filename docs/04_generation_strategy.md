# 04 — Generation Strategy

## Priority Order for Reading Files (at session start)

1. `geniecode/KNOWLEDGE_BASE.md` — Fast context loader (ALWAYS read first)
2. `geniecode/DOMAIN_RULES.md` — Operational SQL rules
3. `geniecode/FILE_FORMATS.md` — Format specs for all asset types
4. `geniecode/TABLE_SCHEMAS.md` — Schema reference
5. `instructions/general.md` — Current general instructions
6. `instruction_library/activation/limits.yml` — Capacity budget
7. Other files as needed for the specific task

## Authoring Model

### Three-Layer Model
```
instruction_library/corpus/     <- Full corpus (superset, authoritative)
         |
         | activation manifests (allowlist)
         v
instructions/                   <- Active deploy surface (materialized)
         |
         | push_folder_to_room.py
         v
Genie Room API                  <- Live room
```

### Split Authoring Surfaces
- **general.md** — Stable room-wide rules (grain, date logic, KPI definitions)
- **example_sql/** — Question-specific patterns (each answering a distinct question)
- **filters/** — Dimension and temporal filter snippets
- **measures/** — KPI calculation snippets

## Capacity-Aware Generation Flow

1. Check current capacity: `python scripts/materialize.py --check-limits`
2. Author new assets in `instruction_library/corpus/<type>/`
3. Update activation manifests if activating
4. Run `python scripts/materialize.py` to update `instructions/`
5. Run `python scripts/validate.py` — must return 0 errors
6. If at capacity: run snippet health check and deactivate lower-priority items
7. Deploy: `python scripts/push_folder_to_room.py`

## When to Choose Which Asset Type

| Need | Asset Type |
|------|------------|
| Room-wide convention (date logic, grain rules) | `instructions/general.md` |
| Specific Q→SQL pattern for a domain question | `instruction_library/corpus/example_sql/` |
| Reusable WHERE clause fragment | `instruction_library/corpus/filters/` |
| Reusable SELECT expression (KPI) | `instruction_library/corpus/measures/` |
| Reusable SELECT expression (dimension) | `instructions/sql_snippets/dimensions/` |
| Ground-truth accuracy pair | `benchmarks/` |
