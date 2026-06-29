# Self-Update Protocol — {{ROOM_NAME}}
> Execute this protocol when the user says "update your knowledge base" or "rescan the repo".

---

## Trigger Phrases
- "update your knowledge base"
- "refresh your context"
- "rescan the repo"
- "sync your knowledge"
- "refresh geniecode"

## Protocol Steps

### Step 1: Scan for Structural Changes
Read these directories and compare counts to the baseline in KNOWLEDGE_BASE.md:

| What to scan | Path |
|-------------|------|
| Kit root | `{{KIT_ROOT_PATH}}` |
| benchmarks/ | `benchmarks/` |
| instructions/example_sql/ | `instructions/example_sql/` |
| instructions/sql_snippets/filters/ | `instructions/sql_snippets/filters/` |
| instructions/sql_snippets/measures/ | `instructions/sql_snippets/measures/` |
| instruction_library/corpus/example_sql/ | `instruction_library/corpus/example_sql/` |
| instruction_library/activation/ | `instruction_library/activation/` |
| metadata/columns/ | `metadata/columns/` |
| data_sources/ | `data_sources/` |
| geniecode/ | `geniecode/` |

### Step 2: Read Configuration Files
Always re-read:
- `room.config.yml`
- `data_sources/tables.yml`
- `instructions/general.md`
- `instructions/general_enriched.md` (if exists)
- `AGENTS.md`

### Step 3: Check Column Metadata
Re-read `metadata/columns/<table>.yml` for each table in `data_sources/tables.yml`.

### Step 4: Check Activation Manifests
Re-read:
- `instruction_library/activation/filters.active.yml`
- `instruction_library/activation/measures.active.yml`
- `instruction_library/activation/example_sql.active.yml`
- `instruction_library/activation/limits.yml`

### Step 5: Spot-Check New Assets
If new files found, read 2-3 samples for format compliance.

### Step 6: Update All geniecode Files
Rewrite: KNOWLEDGE_BASE.md, DOMAIN_RULES.md, TABLE_SCHEMAS.md, FILE_FORMATS.md, SELF_UPDATE.md, BENCHMARK_WORKSPACE.md, FIX_PATTERNS.md, SELECT_STRATEGY.md.

### Step 7: Report to User
- What changed (counts, rules, structure)
- Any issues found
- Confirmation that knowledge base is current

---

## Templates Reference

| Template | Path |
|----------|------|
| benchmark | docs/templates/benchmark.template.yml |
| example_sql | docs/templates/example_sql.template.yml |
| filter_snippet | docs/templates/filter_snippet.template.yml |
| measure_snippet | docs/templates/measure_snippet.template.yml |
| column_metadata | docs/templates/column_metadata.template.yml |
