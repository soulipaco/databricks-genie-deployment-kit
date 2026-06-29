# 01 — Room Asset Map
> **Last updated:** {{UPDATE_DATE}}
> Map of all deployed room assets (what actually gets sent to the Genie API).

## Deployed Assets

### General Instruction
- **File:** `instructions/general.md`
- **Deployed as:** Single text instruction (ID: auto-generated)
- **Purpose:** Room-wide SQL rules, grain logic, KPI conventions

### Example SQL
- **Directory:** `instructions/example_sql/`
- **Count:** {{EXAMPLE_SQL_COUNT}}
- **Budget:** 100 - 1 (general) - {{TABLE_COUNT}} (tables) = {{BUDGET}} slots
- **Purpose:** Question→SQL pairs for Genie to learn from

### Filter Snippets
- **Directory:** `instructions/sql_snippets/filters/`
- **Count:** {{FILTER_COUNT}} active
- **Purpose:** WHERE clause fragments for dimension filtering

### Measure Snippets
- **Directory:** `instructions/sql_snippets/measures/`
- **Count:** {{MEASURE_COUNT}} active
- **Purpose:** SELECT expressions for KPI calculation

### Table Descriptions
- **File:** `data_sources/tables.yml`
- **Count:** {{TABLE_COUNT}} tables
- **Purpose:** Tell Genie what tables are available and what they contain

### Benchmarks
- **Directory:** `benchmarks/`
- **Count:** {{BENCHMARK_COUNT}}
- **Purpose:** Ground-truth Q&A pairs for accuracy evaluation

### Sample Questions
- **In:** `room.config.yml` → `sample_questions`
- **Count:** {{SAMPLE_Q_COUNT}} (typically 5)
- **Purpose:** Conversation starters shown in the Genie UI

## Not Deployed to API
These exist locally only:
- `instruction_library/` — full corpus (superset of deployed)
- `instructions/sql_snippets/dimensions/` — repo-only helper layer
- `geniecode/` — agent knowledge sidecar
- `docs/` — policy documentation
- `snapshots/` — bootstrap artifacts
- `build/` — generated outputs
