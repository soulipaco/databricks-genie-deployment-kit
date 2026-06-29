# Changelog

All notable changes to the Genie Room Deployment Kit are documented here.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

---

## [1.1.0] — 2026-06-19

### Added — Reports System

A complete stakeholder communication and UAT review layer in `reports/`:

- `reports/scripts/generate_inventory.py` — **NEW script** that auto-scans the kit (YAMLs, metadata) and generates all 7 JSON data files in `reports/data/`. Also writes starter markdown summary stubs in `reports/summaries/` if they do not already exist.
- `reports/scripts/generate_report.py` — Reads all 7 markdown summaries and produces a styled HTML report with optional PDF output (weasyprint or pdfkit engines). Includes full CSS (A4, table of contents, cover page).
- `reports/data/` — Output directory for auto-generated JSON inventory files:
  - `room_identity.json` — Room name, space ID, capacity budget, asset counts
  - `domain_capabilities.json` — All active example SQL with parameters and usage_guidance
  - `benchmark_inventory.json` — All benchmark test cases with status
  - `snippet_inventory.json` — All filters, measures, dimensions
  - `evaluation_history.json` — Evaluation session results from `build/eval_*.yml`
  - `sales_ready_questions.json` — Question catalog with trigger phrases
  - `data_sources.json` — Full schema reference from `data_sources/tables.yml` + column metadata
- `reports/summaries/` — 7 markdown summary templates with `{{PLACEHOLDER}}` syntax (auto-populated by `generate_inventory.py`):
  - `00_sales_ready_overview.md` — Capability matrix + question catalog (sales audience)
  - `01_executive_summary.md` — Management overview and room health
  - `02_domain_capabilities.md` — Per-table schema and question templates
  - `03_benchmark_coverage.md` — Ground-truth test coverage
  - `04_evaluation_progress.md` — Evaluation timeline, pass rate, failure distribution
  - `05_data_source_reference.md` — Full schema reference with semantic measures
  - `06_fix_history_and_patterns.md` — Engineering work log and pattern library
- `reports/UAT_Reports/` — Operations sign-off review package:
  - `README.md` — Reviewer instructions and sign-off status table
  - `summaries/00_overview_and_objectives.md` — Review process and sign-off criteria
  - `summaries/01_data_validation_checklist.md` — KPI accuracy validation table
  - `summaries/02_genie_qa_checklist.md` — Q&A checklist by question category
  - `summaries/03_insights_action_plans_checklist.md` — Insight quality review
  - `scripts/generate_uat_report.py` — Generates UAT guide as HTML/PDF

### Added — Skill

- `skills/generate_reports/SKILL.md` — 15th skill: 10-step runbook (inventory → summarize → generate report → generate UAT guide), covering all 4 phases and report audiences

### Changed

- `AGENTS.md` — Kit structure tree updated with `reports/` directory; Skills Reference table now lists `generate_reports` (15 total skills)

---

## [1.0.0] — 2026-06-19

### Added — Framework Architecture
- `room.config.yml` — Unified room configuration template with full `{{PLACEHOLDER}}` syntax, replacing the fragmented approach of earlier versions
- `AGENTS.md` — Complete AI coding agent instruction manual with Genie API reference, file format specs, and task runbooks
- `README.md` — Human-readable overview and quick-start guide

### Added — Skill System (14 Skills)
All skills follow the 6-section format: trigger → inputs → steps → outputs → validation → references
- `configure_new_room` — Bootstrap a new Genie room from template
- `add_data_source` — Register a new Unity Catalog table as a metric view source
- `generate_measures` — Generate SQL measure snippets from column metadata
- `generate_filters` — Generate SQL filter snippets from column metadata
- `generate_example_sql` — Generate example SQL files for benchmark coverage
- `generate_benchmarks` — Generate benchmark question YAML files
- `health_check` — Comprehensive room asset validation
- `migrate_data_source` — Migrate a room from one data source to another
- `promote_to_instruction` — Promote a corpus snippet to active deployment
- `run_benchmark_evaluation` — Execute a batch benchmark evaluation
- `analyze_benchmark_failures` — Triage failures and produce fix recommendations
- `manage_capacity` — Review and rebalance instruction capacity budget
- `sync_room` — Bidirectional push/pull sync between folder and live room
- `update_geniecode` — Update agent knowledge sidecar after domain changes

### Added — GenieCode Agent Knowledge Sidecar
Complete agent knowledge system in `geniecode/`:
- `KNOWLEDGE_BASE.md` — Single-file fast context loader (read first every session)
- `DOMAIN_RULES.md` — Operational rules for SQL generation in this room
- `FIX_PATTERNS.md` — Known failure patterns with symptom → root cause → fix → validation
- `BENCHMARK_WORKSPACE.md` — Benchmark evaluation framework with 7-class failure taxonomy
- `BENCHMARK_UPDATE_PROCEDURES.md` — 10-step decision flowchart for benchmark fixes
- `SELF_UPDATE.md` — Self-update protocol for refreshing geniecode/ files
- `TABLE_SCHEMAS.md` — Schema reference for all data tables
- `FILE_FORMATS.md` — YAML/MD format specs for every asset type
- `SNIPPET_HEALTH_CHECK.md` — Snippet audit procedures (7 check categories)
- `SELECT_STRATEGY.md` — Decision guide for table and snippet selection
- `scripts/snippet_health_check.py` — Executable health check script (7 checks: CHK-1 through CHK-7)

### Added — Instruction Library Pipeline
- `instruction_library/corpus/` — Full instruction corpus (superset of deployed set)
- `instruction_library/activation/` — Allowlist manifests + capacity budget (limits.yml)
- `instruction_library/reduction/` — Merge/isolation decision records
- `instruction_library/isolated/` — Deactivated snippet ID manifests
- `scripts/materialize.py` — Materializes corpus → active instructions/

### Added — Python Automation Scripts
Real executable Python 3.x scripts in `scripts/`:
- `materialize.py` — Materialize instruction_library → instructions/
- `validate.py` — Validate deployment kit structure (0 errors required)
- `prepare_eval.py` — Prepare benchmark evaluation batches
- `freeze.py` — Snapshot current instruction state
- `push_folder_to_room.py` — Deploy local folder → Genie room via API
- `pull_room_to_folder.py` — Pull Genie room → local folder
- `analyze_benchmarks.py` — Analyze evaluation results and produce failure taxonomy
- `snippet_health_check.py` — Health check all snippets (also in geniecode/scripts/)

### Added — Policy Documentation (19 numbered docs + phase workflows)
Complete policy library in `docs/`:
- `00_repo_inventory.md` through `18_general_instruction_production_workflow.md`
- `phase_01_repo_discovery.md` — Discover and map an existing room repository
- `phase_01_authoring_workflow.md` — Author new room assets from scratch
- `phase_02_evaluation_workflow.md` — Benchmark evaluation and iteration workflow
- `cap_management/` — Capacity management documentation (9 files)
- `contracts/` — Semantic contracts per metric view (3 example contracts)
- `knowledge/` — Accumulated usage guidance and promotion candidates (9 files)
- `templates/` — Authoring templates for every asset type (11 files)

### Added — Asset Templates (14 templates)
All templates in `templates/` with `{{PLACEHOLDER}}` syntax:
- `measure_simple.yml`, `measure_ratio.yml` — Measure snippet templates
- `filter_dimension.yml`, `filter_temporal.yml` — Filter snippet templates
- `benchmark.yml`, `example_sql.yml` — Benchmark and example SQL templates
- `column_metadata.yml` — Column metadata configuration template
- `instruction_snippet.yml` — Generic instruction library snippet template
- `activation_manifest.yml` — Activation allowlist manifest template
- `benchmark_batch.yml` — Batch benchmark evaluation config template
- `question_batch.yml` — Question batch generation config template
- `room.config.tpl` — Room configuration scaffold template
- `data_sources_tables.yml` — Data sources table registration template
- `limits.yml` — Capacity budget limits template

### Added — Environment Support
- `env/local.yml` — Local development environment configuration
- `env/prod.yml` — Production environment configuration

### Added — Worked Example
Fully worked sample.sales example in `examples/sample_sales_analytics/`:
- Room config, data sources, metadata, instructions, benchmarks, activation, geniecode
- 3 filter snippets, 3 measure snippets, 1 dimension snippet
- 3 example SQL files
- 5 benchmark questions
- Sample deployment readiness report and evaluation summary

### Notes
This release consolidates the reusable deployment-kit framework, instruction
library pipeline, reporting layer, and worked example into a public,
domain-neutral package.
