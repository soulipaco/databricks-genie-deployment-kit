# AGENTS.md — Genie Room Deployment Kit

> This file tells AI coding agents how to navigate, modify, and extend any Genie Room Deployment Kit.
> It is room-agnostic — the same conventions apply regardless of which Genie space this kit manages.

---

## What Is This Kit?

A **Genie Room Deployment Kit** manages a Databricks Genie space (AI data room) as code. Instead of editing a room manually through the UI, the room's entire configuration is stored as modular YAML and Markdown files.

Two companion scripts handle syncing:
- **scripts/pull_room_to_folder.py** — Exports the live Genie room → overwrites local files.
- **scripts/push_folder_to_room.py** — Validates + assembles local files → deploys to the live room via API.

The **folder files are the source of truth** once bootstrapped:
- `instruction_library/` is the canonical source of truth for the full instruction corpus.
- `instructions/` is the active deploy surface generated from that library.

Direct UI edits should be pulled back into the folder to stay in sync.

---

## Kit Structure

```
<kit_root>/
├── AGENTS.md                        # ← You are here
├── room.config.yml                  # Room-level config (template with {{PLACEHOLDERS}})
├── README.md                        # Human-readable overview
├── CHANGELOG.md                     # Version history
├── data_sources/
│   └── tables.yml                   # Unity Catalog table references
├── metadata/
│   └── columns/
│       └── <table>.yml              # Per-table column configs
├── instruction_library/             # Canonical full instruction corpus + activation manifests
│   ├── README.md
│   ├── corpus/                      # All possible snippets (superset of deployed)
│   │   ├── filters/
│   │   ├── measures/
│   │   ├── dimensions/
│   │   └── example_sql/
│   ├── activation/                  # Allowlist manifests + capacity limits
│   │   ├── filters.active.yml
│   │   ├── measures.active.yml
│   │   ├── dimensions.active.yml
│   │   ├── example_sql.active.yml
│   │   └── limits.yml
│   ├── reduction/                   # Merge/isolation decision records
│   └── isolated/                    # Deactivated ID manifests
├── instructions/                    # Active deploy surface (materialized from library)
│   ├── general.md                   # Deployed general instructions
│   ├── general_enriched.md          # Enriched version with extra context
│   ├── example_sql/                 # Active deployable example SQL subset
│   └── sql_snippets/
│       ├── filters/                 # Active deployable filter subset
│       ├── measures/                # Active deployable measure subset
│       └── dimensions/              # Repo-only helper layer for reusable output fields
├── benchmarks/                      # Ground-truth question → SQL pairs for accuracy testing
├── env/
│   ├── local.yml                    # Local dev environment config
│   └── prod.yml                     # Production environment config
├── snapshots/                       # Bootstrap artifacts (read-only reference)
├── build/                           # Generated payloads (ephemeral, do not edit)
│   └── deployment_readiness/
├── scripts/                         # Python automation scripts
│   ├── materialize.py               # Materialize instruction_library → instructions/
│   ├── validate.py                  # Validate deployment kit structure
│   ├── prepare_eval.py              # Prepare benchmark evaluation batches
│   ├── freeze.py                    # Snapshot current instruction state
│   ├── push_folder_to_room.py       # Deploy folder → Genie room
│   ├── pull_room_to_folder.py       # Pull Genie room → folder
│   ├── analyze_benchmarks.py        # Analyze evaluation results
│   └── snippet_health_check.py      # Health check all snippets
├── reports/                         # Stakeholder reporting and UAT review layer
│   ├── README.md                    # Reporting system overview
│   ├── data/                        # Auto-generated JSON inventory (run generate_inventory.py)
│   │   ├── room_identity.json        # Room metadata and capacity
│   │   ├── domain_capabilities.json  # All example SQL with parameters
│   │   ├── benchmark_inventory.json  # All benchmark test cases
│   │   ├── snippet_inventory.json    # All active filters/measures/dimensions
│   │   ├── evaluation_history.json   # Evaluation session results
│   │   ├── sales_ready_questions.json# Question catalog with trigger phrases
│   │   └── data_sources.json         # Full schema reference
│   ├── summaries/                    # Markdown reports (human-authored/auto-stub)
│   │   ├── 00_sales_ready_overview.md
│   │   ├── 01_executive_summary.md
│   │   ├── 02_domain_capabilities.md
│   │   ├── 03_benchmark_coverage.md
│   │   ├── 04_evaluation_progress.md
│   │   ├── 05_data_source_reference.md
│   │   └── 06_fix_history_and_patterns.md
│   ├── scripts/
│   │   ├── generate_inventory.py     # Scans kit → generates data/*.json + summary stubs
│   │   └── generate_report.py        # Reads summaries/*.md → HTML/PDF report
│   └── UAT_Reports/                  # Operations sign-off review package
│       ├── README.md
│       ├── summaries/                # UAT checklists
│       └── scripts/
│           └── generate_uat_report.py
├── geniecode/                       # Agent knowledge sidecar (read every session)
│   ├── KNOWLEDGE_BASE.md            # Fast context loader — READ THIS FIRST
│   ├── DOMAIN_RULES.md              # Operational rules for SQL generation
│   ├── FIX_PATTERNS.md              # Known failure patterns and proven fixes
│   ├── BENCHMARK_WORKSPACE.md       # Benchmark evaluation framework
│   ├── BENCHMARK_UPDATE_PROCEDURES.md # Step-by-step benchmark fix playbook
│   ├── SELF_UPDATE.md               # Protocol for updating geniecode/
│   ├── TABLE_SCHEMAS.md             # Schema reference for all data tables
│   ├── FILE_FORMATS.md              # YAML/MD format specs for every asset type
│   ├── SNIPPET_HEALTH_CHECK.md      # Snippet audit procedures and check categories
│   ├── SELECT_STRATEGY.md           # Decision guide for table/snippet selection
│   └── scripts/
│       └── snippet_health_check.py  # Executable health check script
├── docs/                            # Policy library and operational docs
│   ├── README.md
│   ├── 00_repo_inventory.md
│   ├── 01_room_asset_map.md
│   ├── 02_reference_asset_map.md
│   ├── 03_placeholder_vs_real_content.md
│   ├── 04_generation_strategy.md
│   ├── 05_metric_view_contract_summary.md
│   ├── 06_question_taxonomy.md
│   ├── 07_question_generation_rules.md
│   ├── 08_asset_generation_playbook.md
│   ├── 09_benchmark_question_bank.md
│   ├── 10_evaluation_adjustment_workflow.md
│   ├── 11_failed_evaluation_tracking.md
│   ├── 12_usage_guidance_skeleton.md
│   ├── 13_usage_guidance_migration_policy.md
│   ├── 14_filter_instruction_skeleton.md
│   ├── 15_filter_migration_policy.md
│   ├── 16_measure_instruction_skeleton.md
│   ├── 17_measure_migration_policy.md
│   ├── 18_general_instruction_production_workflow.md
│   ├── phase_01_repo_discovery.md
│   ├── phase_01_authoring_workflow.md
│   ├── phase_02_evaluation_workflow.md
│   ├── cap_management/
│   ├── contracts/
│   ├── knowledge/
│   └── templates/
├── skills/                          # Skill definitions for AI coding agents
│   └── <skill_name>/SKILL.md
├── templates/                       # Asset templates with {{PLACEHOLDER}} syntax
│   └── *.yml
└── examples/                        # Fully worked sample.sales example
    └── sample_sales_analytics/
```

---

## Safety Rules

### Never Do
- **Never manually edit `build/`** — generated outputs only; regenerated during assembly.
- **Never edit `snapshots/`** — read-only bootstrap artifacts.
- **Never assume `instructions/dimensions/` is deployable** — it is a repo-only helper layer.
- **Never hard-code dates** in SQL. Use `:StartDate`/`:EndDate` parameters or dynamic expressions (`CURRENT_DATE()`, `DATE_ADD()`, etc.).
- **Never duplicate IDs** across example_sql, benchmarks, or sql_snippets. Each `id` is a 32-char hex string, globally unique within the room.
- **Never remove a file** from `example_sql/`, `benchmarks/`, `filters/`, or `measures/` without checking that assembly uses glob patterns — missing files silently reduce room content.
- **Never point `room.config.yml` or `push_folder_to_room.py` at `instruction_library/`** — the deploy contract uses `instructions/`.
- **Never embed env-specific values** (workspace URLs, warehouse IDs, space IDs) in room content files — those belong in `env/*.yml` only.

### Always Do
- **Validate after every structural change** — run `python scripts/validate.py` and check for 0 errors.
- **Prepare before every push** — run `python scripts/prepare_eval.py` and deploy only when gate reports READY.
- **Preserve `_cleanup_flags`** in YAML files — these mark known issues (hard-coded dates, etc.). Remove only after fixing the underlying issue.
- **Keep file naming consistent** — numbered prefix (`01_`, `02_`, ...) followed by a slug, `.yml` extension.
- **Use `ILIKE '%value%'`** for all text-based filters (case-insensitive matching is a cross-room convention).
- **Include all filter fields in SELECT** — if a query filters on a column, that column must appear in the output.

---

## File Format Reference

### room.config.yml
```yaml
room_name: {{ROOM_NAME}}
title: {{ROOM_DISPLAY_TITLE}}
description: |-
  {{ROOM_DESCRIPTION}}
version: 2
purpose: {{ROOM_PURPOSE}}
source_of_truth: repo
parent_path: {{WORKSPACE_PARENT_PATH}}
sample_questions:
  - id: {{32_CHAR_HEX_ID}}
    question: {{SAMPLE_QUESTION_TEXT}}
data_sources: data_sources/tables.yml
column_metadata: metadata/columns/
instructions:
  general: instructions/general.md
  example_sql: instructions/example_sql/
  sql_snippets:
    filters: instructions/sql_snippets/filters/
    measures: instructions/sql_snippets/measures/
benchmarks: benchmarks/
bootstrap_snapshot: snapshots/exported_space.json
```

### data_sources/tables.yml
```yaml
tables:
  - identifier: catalog.schema.table_name    # Must be 3-level fully qualified
    description: <what this table contains>
    column_metadata_file: metadata/columns/table_name.yml
```

### metadata/columns/<table>.yml
```yaml
table: catalog.schema.table_name
columns:
  - column_name: <name>
    exclude: true                    # Hide from Genie (optional)
    enable_format_assistance: true   # Help with formatting (optional)
    enable_entity_matching: true     # Enable fuzzy matching (optional)
    get_example_values: true         # Fetch sample values (optional)
    build_value_dictionary: true     # Build value lookup (optional)
```

### instructions/example_sql/<NN>_<slug>.yml
```yaml
id: <32-char hex>                    # Generate: import uuid; uuid.uuid4().hex
question: <natural language question>
sql: <SQL query string>
parameters:                          # Optional
  - name: StartDate
    type_hint: DATE
  - name: EndDateExclusive
    type_hint: DATE
  - name: PeriodMode
    type_hint: INTEGER
usage_guidance: |                    # Optional - when/how Genie should use this
  Use for ... Bind PeriodMode to ...
_cleanup_flags: ['2025-03-01']       # Optional - hard-coded dates to fix
```

### instructions/sql_snippets/filters/<NN>_<slug>.yml
```yaml
id: <32-char hex>
display_name: <human-readable name>
sql: <WHERE clause fragment - NO 'WHERE' keyword, just conditions>
synonyms: [alias1, alias2]           # Optional
instruction: |                       # Optional
  WHEN_TO_USE: Apply when user filters by <dimension>.
  SCOPE_TABLES: <table_name>.
  TIMEFRAME_HINT: <applicable time range, or 'any'>.
  RISK_IF_MISUSED: <what goes wrong if applied incorrectly>.
```

### instructions/sql_snippets/measures/<NN>_<slug>.yml
```yaml
id: <32-char hex>
alias: <column alias>
display_name: <human-readable name>
sql: <SELECT expression - aggregation formula>
synonyms: [alias1, alias2]           # Optional
instruction: |                       # Optional
  WHEN_TO_USE: ...
  SCOPE_TABLES: ...
  RISK_IF_MISUSED: ...
```

### instructions/sql_snippets/dimensions/<NN>_<slug>.yml
```yaml
id: <32-char hex>
alias: <column alias>
display_name: <human-readable name>
sql: <SELECT expression for reusable output field>
instruction: <when to use, scope, risks>
```

`instructions/dimensions/` is a repo-only helper layer for reusable output fields such as period boundaries, grain labels, and explanation helpers. It is NOT part of the current room deploy payload.

### benchmarks/<NN>_<slug>.yml
```yaml
id: <32-char hex>
question: <natural language question>
answer_format: SQL
sql: <ground-truth SQL>
_cleanup_flags: [...]                # Optional
```

### env/<environment>.yml
```yaml
environment: <name>                  # local, staging, prod
workspace_url: https://{{WORKSPACE_HOST}}
warehouse_id: {{SQL_WAREHOUSE_ID}}
space_id: {{GENIE_SPACE_ID}}         # null for new room
parent_path: {{WORKSPACE_FOLDER_PATH}}
```

### instructions/general.md
```markdown
# General Instructions

> **Source ID:** `<id>`
> Auto-extracted from Genie room `<name>`. Edit this file as the source of truth.

---

<Free-text instructions for the Genie LLM: grain logic, KPI rules,
aggregation conventions, date handling, formatting rules, etc.>
```

### instruction_library/activation/<type>.active.yml
```yaml
asset_type: <filters|measures|dimensions|example_sql>
active_ids:
  - <32-char hex>   # 01_snippet_slug.yml
  - <32-char hex>   # 02_snippet_slug.yml
```

### instruction_library/activation/limits.yml
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

---

## Common Tasks

### Add a new example SQL
1. Create `instruction_library/corpus/example_sql/NN_slug.yml` with `id`, `question`, `sql`.
2. Generate a unique ID: `python -c "import uuid; print(uuid.uuid4().hex)"`
3. Add `parameters` if the query uses `:ParamName` placeholders.
4. Add `usage_guidance` explaining when Genie should use this query.
5. Add the ID to `instruction_library/activation/example_sql.active.yml` only if it should be active.
6. Run `python scripts/materialize.py` to update `instructions/`.
7. Run `python scripts/validate.py` to verify 0 errors.

### Add a new benchmark
Same as example SQL but in `benchmarks/` with `answer_format: SQL` and ground-truth `sql`.

### Add a new table
1. Add entry to `data_sources/tables.yml` with full 3-level identifier.
2. Create `metadata/columns/<table_name>.yml` with column configs.
3. Update `instructions/general.md` if the table has special grain logic or join rules.
4. Run `python scripts/validate.py`.

### Add a filter snippet
1. Create `instruction_library/corpus/filters/NN_slug.yml`.
2. `sql` should be a WHERE clause fragment (no `WHERE` keyword, just conditions).
3. Add `instruction` with WHEN_TO_USE, SCOPE_TABLES, TIMEFRAME_HINT, RISK_IF_MISUSED.
4. Add ID to `instruction_library/activation/filters.active.yml` if active now.
5. Run `python scripts/materialize.py && python scripts/validate.py`.

### Add a measure snippet
1. Create `instruction_library/corpus/measures/NN_slug.yml`.
2. `sql` should be a SELECT expression (aggregation formula).
3. Set `alias` to the output column name.
4. Add ID to `instruction_library/activation/measures.active.yml` if active now.
5. Run `python scripts/materialize.py && python scripts/validate.py`.

### Fix a hard-coded date
1. Find files with `_cleanup_flags` containing date strings.
2. Replace literal dates with `:StartDate`/`:EndDate` parameters or `CURRENT_DATE()` expressions.
3. Add parameter definitions if not present.
4. Remove fixed values from `_cleanup_flags`. Delete the key if array becomes empty.

### Run benchmark evaluation
See `skills/run_benchmark_evaluation/SKILL.md` for the full procedure.

### Fix a failed benchmark
See `geniecode/BENCHMARK_UPDATE_PROCEDURES.md` for the 10-step decision flowchart.

### Manage capacity
See `docs/cap_management/01_instruction_capacity_overview.md` for capacity management.

### Sync with room
```bash
# Pull latest from live room
python scripts/pull_room_to_folder.py

# Edit canonical files as needed
# (modify instruction_library/ and canonical docs)

# Materialize and validate
python scripts/materialize.py
python scripts/validate.py

# Push changes to live room
python scripts/push_folder_to_room.py
```

---

## Genie API Reference

### Endpoints
- `GET  /api/2.0/genie/spaces/{space_id}?include_serialized_space=true` — read room config
- `POST /api/2.0/genie/spaces` — create new room
- `PUT  /api/2.0/genie/spaces/{space_id}` — update existing room
- `PATCH /api/2.0/genie/spaces/{space_id}` — partial update

### Authentication (inside Databricks workspace)
```python
ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
host = "https://" + ctx.browserHostName().get()
token = ctx.apiToken().get()
```

### Payload Structure
The API expects: `{title, description, warehouse_id, parent_path, serialized_space}`
where `serialized_space` is a JSON string containing:
```json
{
  "version": 2,
  "config": {"sample_questions": [{"id": "...", "question": ["..."]}]},
  "data_sources": {"tables": [{"identifier": "...", "column_configs": [...]}]},
  "instructions": {
    "text_instructions": [{"id": "...", "content": ["..."]}],
    "example_question_sqls": [{"id": "...", "question": ["..."], "sql": ["..."]}],
    "sql_snippets": {"filters": [...], "measures": [...], "expressions": [...]}
  },
  "benchmarks": {"questions": [{"id": "...", "question": ["..."], "answer": [{"format": "SQL", "content": ["..."]}]}]}
}
```

**Key convention:** The API wraps most string values in single-element arrays (`["text"]`).
- When reading from API → unwrap: `val[0]`
- When writing to API → wrap: `[val]`

**Sorting:** The API requires sorted arrays by `id` for tables, example_sqls, filters, measures, benchmarks, and sample_questions.

### Type Hint Mapping
```python
TYPE_HINT_MAP = {
    "INT": "INTEGER",
    "FLOAT": "DOUBLE",
    "BOOL": "BOOLEAN",
    "STR": "STRING",
}
```

---

## Benchmark Evaluation Lifecycle

### 1. Prepare
```bash
python scripts/prepare_eval.py --output build/eval_batch.yml
```
Outputs a batch of benchmarks to evaluate.

### 2. Evaluate
Run the Genie room against each benchmark question. Record:
- Question text
- Model SQL output
- Ground truth SQL
- Pass/Fail assessment
- Score reason

### 3. Triage
For each failure, follow the 7-class taxonomy in `geniecode/BENCHMARK_WORKSPACE.md`:
1. OUTPUT-SHAPE — correct logic, wrong output format
2. SEMANTIC-GENERATION — wrong metric/grain/logic
3. BENCHMARK-DEFECT — ground truth is wrong
4. EVALUATOR-FRAGILITY — false negative from evaluator
5. MIXED — both GT and model have issues
6. RETRIEVAL-COLLISION — model retrieved wrong example SQL
7. SNIPPET-CONTRADICTION — snippet guidance contradicts itself

### 4. Fix
Follow `geniecode/BENCHMARK_UPDATE_PROCEDURES.md` 10-step decision flowchart.

### 5. Validate and Deploy
```bash
python scripts/materialize.py
python scripts/validate.py
python scripts/push_folder_to_room.py
```

### 6. Re-evaluate
Run the evaluation again on previously failed benchmarks to confirm fixes.

---

## Capacity Management

The Genie API has a limit on total instructions per room (default: 100).

**Budget allocation:**
```
Total budget:           100 instructions
General instruction:     -1
Table descriptions:      -N (one per table)
Available for snippets:  100 - 1 - N
```

**Per-type budgets** (configured in `instruction_library/activation/limits.yml`):
- `example_sql`: derived from total minus general minus tables
- `filters`: max 100 (separate budget)
- `measures`: max 100 (separate budget)

**When at capacity:**
1. Run `python scripts/snippet_health_check.py --mode full --fix-plan` to find duplicates.
2. Review `docs/cap_management/` for isolation and similarity analysis.
3. Deactivate lower-value snippets by removing their IDs from `instruction_library/activation/*.active.yml`.
4. Add deactivated IDs to `instruction_library/isolated/*.isolated.yml`.

---

## Instruction Library Pipeline

```
instruction_library/corpus/    ← Authoring surface (full superset)
         │
         │ activation/*.active.yml (allowlist)
         │ activation/limits.yml (capacity budget)
         ↓
scripts/materialize.py         ← Runs materialization
         │
         ↓
instructions/                  ← Deploy surface (active subset)
         │
         │ scripts/push_folder_to_room.py
         ↓
Genie Room API                 ← Live room
```

**Rule:** NEVER add to `instructions/` directly. Always author in `instruction_library/corpus/` first, then activate via manifest, then materialize.

---

## Testing Checklist

After any change, verify:
1. Validation returns 0 errors: `python scripts/validate.py`
2. Assembly produces valid payload with correct component counts.
3. No new hard-coded dates introduced.
4. All `id` fields remain unique across their category.
5. File naming follows `NN_slug.yml` convention.
6. New tables have matching column metadata files.
7. All text filters use `ILIKE '%value%'` pattern.
8. Capacity limits not exceeded: `python scripts/materialize.py --check-limits`.
9. Snippet health is clean: `python scripts/snippet_health_check.py --mode full`.

---

## Skills Reference

Each skill in `skills/<name>/SKILL.md` provides a 6-section executable runbook:

| Skill | Trigger | Purpose |
|-------|---------|--------|
| `configure_new_room` | "set up a new room" | Bootstrap from room.config.yml template |
| `add_data_source` | "add a table" | Register a new metric view source |
| `generate_measures` | "generate measures" | Create measure snippets from column metadata |
| `generate_filters` | "generate filters" | Create filter snippets from column metadata |
| `generate_example_sql` | "generate examples" | Create example SQL files for benchmarks |
| `generate_benchmarks` | "generate benchmarks" | Create benchmark question YAML files |
| `health_check` | "run health check" | Comprehensive room asset validation |
| `migrate_data_source` | "migrate the data source" | Switch from one table to another |
| `promote_to_instruction` | "promote this snippet" | Move from corpus to active deployment |
| `run_benchmark_evaluation` | "run benchmarks" | Execute evaluation batch and produce report |
| `analyze_benchmark_failures` | "analyze failures" | Triage failures and recommend fixes |
| `manage_capacity` | "check capacity" | Review and rebalance instruction budget |
| `sync_room` | "push to room" / "pull from room" | Bidirectional room sync |
| `update_geniecode` | "update knowledge base" | Refresh geniecode/ after domain changes |
| `generate_reports` | "generate the report" / "generate inventory" | Auto-generate inventory JSON + HTML/PDF reports + UAT guide |
| `pipeline_configure` | "configure the pipeline" | Fill all `pipeline_config.yml` placeholders before first run |
| `pipeline_setup` | "set up the pipeline" | Full first-time setup: generate PDFs → upload → VS index → workflow |
| `pipeline_add_domain` | "add a domain to the pipeline" | Add new category across all 4 required locations simultaneously |
| `pipeline_update_playbook` | "update the playbook" | Edit scenarios/cards, regenerate PDF, re-upload, re-sync index |

---

## GenieCode Knowledge Sidecar

The `geniecode/` directory is a self-contained knowledge base for AI coding agents. Read it at the start of every session.

**Reading order:**
1. `geniecode/KNOWLEDGE_BASE.md` — Fast context loader (read FIRST every session)
2. `geniecode/DOMAIN_RULES.md` — Operational SQL rules for this room
3. `geniecode/FILE_FORMATS.md` — Format specs for every asset type
4. `geniecode/TABLE_SCHEMAS.md` — Schema reference for all data tables
5. Others as needed for specific tasks

**Self-update protocol:** When the user says "update your knowledge base", execute `geniecode/SELF_UPDATE.md`.

---

## Action Plans Pipeline

This kit includes an automated pipeline that generates action plans from Genie trend analysis.
It consists of Databricks notebooks orchestrated by a scheduled workflow.

**Read these docs before touching anything in `pipeline/`, `setup/`, or `pipeline_playbook_generator/`:**

| Doc | Covers |
|---|---|
| [pipeline/docs/01_system_overview.md](pipeline/docs/01_system_overview.md) | End-to-end flow, folder layout, stable contract |
| [pipeline/docs/02_object_map.md](pipeline/docs/02_object_map.md) | Delta table and VS index naming (all derived from config) |
| [pipeline/docs/03_playbook_ingestion_and_chunking.md](pipeline/docs/03_playbook_ingestion_and_chunking.md) | PDF sources, chunking strategy, adding new playbooks |
| [pipeline/docs/04_pipeline_behavior.md](pipeline/docs/04_pipeline_behavior.md) | Notebook-by-notebook behavior, Genie client, LLM prompting |
| [pipeline/docs/05_runbook.md](pipeline/docs/05_runbook.md) | First-time setup sequence, regular operations, cleanup |
| [pipeline/docs/06_change_guide_for_agents.md](pipeline/docs/06_change_guide_for_agents.md) | Recipes for every common change type, validation checklist |

**Single source of truth for all pipeline parameters:**

```
pipeline/pipeline_config.yml
```

Every notebook reads this file at startup and refuses to run if any `{{PLACEHOLDER}}` is unconfigured.
Never hardcode catalog names, table names, endpoints, or paths in notebooks.

**Key cross-notebook contract** — keep these aligned in `pipeline_config.yml`:
- `playbooks.sources[].question_category`
- `questions.seeds[].category`
- `system_prompts` keys

If any one drifts from the others, retrieval produces empty or irrelevant results.

**Playbook generator:**

```bash
python pipeline_playbook_generator/generate_playbook.py --kit-format genie_kit
```

See `pipeline_playbook_generator/README.md` for full usage.
