# Databricks Genie Deployment Kit

A deployment-as-code framework for building, testing, documenting, and operating Databricks Genie spaces.

This repository treats a Genie room like a software product: configuration, semantic rules, examples, benchmark questions, deployment scripts, reporting docs, and agent runbooks all live in version-controlled files.

## Why This Exists

Genie spaces can become hard to maintain when instructions, example SQL, metric definitions, and evaluation questions only live in the UI. This kit moves those assets into a structured repository so they can be reviewed, tested, reused, and redeployed.

The goal is not only to create a Genie room. The goal is to create a repeatable operating model for AI/BI analytics rooms.

## What The Kit Provides

- Template-driven room setup with `room.config.yml`
- Data-source registration through `data_sources/tables.yml`
- Per-column semantic metadata in `metadata/columns/`
- General Genie instructions in Markdown
- Example SQL patterns for high-value business questions
- SQL snippets for measures and filters
- Benchmark questions for evaluation
- Deployment scripts for pushing local assets to Genie
- Reporting and UAT documentation scaffolds
- Agent runbooks in `skills/` and `AGENTS.md`
- Optional action-plan pipeline using Databricks SQL, Vector Search, and LLM endpoints

## Portfolio Demo

The main public demo is:

[examples/olist_ecommerce](examples/olist_ecommerce)

Live dashboard:

[Olist E-Commerce AI/BI Dashboard](https://dbc-5a674036-8eaa.cloud.databricks.com/dashboardsv3/01f173eb9b821ef9b5cf8e6c8ec78028/published?o=7474648785966975)

It uses the public Olist Brazilian E-Commerce dataset and demonstrates:

- raw CSV ingestion to a Unity Catalog Volume
- bronze table creation
- enriched gold analytics tables
- diagnostic tables for Pareto and target-gap analysis
- Genie room deployment from local files
- published AI/BI dashboard with 29 widgets across 8 pages
- benchmark questions for quality checks
- action-plan pipeline example with generated RAG playbook assets
- action playbook generation for Vector Search and LLM-backed recommendations

The deployed demo model includes:

- `workspace.olist_ecommerce.olist_order_metrics_mv`
- `workspace.olist_ecommerce.olist_category_diagnostics_mv`
- `workspace.olist_ecommerce.olist_customer_state_diagnostics_mv`

Example Genie questions:

- What was total order value by month?
- Which product categories have the highest late delivery rate?
- Which product categories make up the top 80 percent of order value?
- How does late delivery affect review score by product category?
- To reach a 4.2 average review score, which categories need the largest late delivery rate reduction?

## What To Review First

For a quick portfolio review:

1. Open the [published AI/BI dashboard](https://dbc-5a674036-8eaa.cloud.databricks.com/dashboardsv3/01f173eb9b821ef9b5cf8e6c8ec78028/published?o=7474648785966975).
2. Read the Olist room package in [examples/olist_ecommerce](examples/olist_ecommerce).
3. Inspect the generated action playbook in [examples/olist_ecommerce/pipeline_playbook_generator/generated/olist_ecommerce_analytics_action_playbook.md](examples/olist_ecommerce/pipeline_playbook_generator/generated/olist_ecommerce_analytics_action_playbook.md).
4. Review the pipeline config in [examples/olist_ecommerce/pipeline/pipeline_config.yml](examples/olist_ecommerce/pipeline/pipeline_config.yml).

## Repository Tour

| Path | Purpose |
|---|---|
| `room.config.yml` | Generic room manifest template |
| `data_sources/` | Table registrations |
| `metadata/columns/` | Per-column semantic configuration |
| `instructions/` | Active Genie instructions, example SQL, and snippets |
| `instruction_library/` | Larger corpus plus activation manifests |
| `benchmarks/` | Ground-truth questions for evaluation |
| `scripts/` | Validation, materialization, push/pull, benchmark tooling |
| `docs/` | Policy docs, authoring workflows, evaluation workflows |
| `geniecode/` | Agent knowledge sidecar for maintaining a room |
| `pipeline/` | Optional action-plan pipeline for trend analysis and recommendations |
| `pipeline_playbook_generator/` | Generates RAG-ready action playbooks |
| `reports/` | UAT and stakeholder reporting scaffolds |
| `examples/` | Worked examples, including the Olist public dataset demo |
| `skills/` | Task runbooks for repeatable operations |

## Quick Start

Validate the generic kit:

```bash
python scripts/validate.py
```

Materialize active instruction-library assets:

```bash
python scripts/materialize.py
```

Deploy a configured room:

```bash
python scripts/push_folder_to_room.py --env local
```

For the Olist demo, use the dedicated deployment guide:

[examples/olist_ecommerce/DEPLOY.md](examples/olist_ecommerce/DEPLOY.md)

## Olist Demo Assets

The Olist example includes:

- [Dataset notes](examples/olist_ecommerce/DATASET.md)
- [Databricks setup status](examples/olist_ecommerce/SETUP_STATUS.md)
- [Enrichment layer docs](examples/olist_ecommerce/ENRICHMENT.md)
- [Genie room deploy script](examples/olist_ecommerce/deploy_genie_room.py)
- [AI/BI dashboard brief](examples/olist_ecommerce/dashboard/dashboard_brief.md)
- [Published dashboard details](examples/olist_ecommerce/dashboard/PUBLISHED_DASHBOARD.md)
- [Starter dashboard SQL](examples/olist_ecommerce/dashboard/starter_queries.sql)
- [Action-plan pipeline example](examples/olist_ecommerce/pipeline/README.md)
- [Generated Olist action playbook](examples/olist_ecommerce/pipeline_playbook_generator/generated/olist_ecommerce_analytics_action_playbook.md)
- Databricks notebook-style scripts in `examples/olist_ecommerce/databricks/`

## Public Dataset Attribution

The Olist demo is based on the Brazilian E-Commerce Public Dataset by Olist:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Check the Kaggle dataset page for the current license and attribution requirements before publishing screenshots, derived extracts, or packaged sample files.

## Security Notes

- Do not commit Databricks tokens.
- Do not commit downloaded raw datasets.
- Keep workspace-specific values in ignored local environment files.
- Use placeholders in public examples where possible.
- Rotate any token that was pasted into chat or terminal history.

## For AI Coding Agents

Read [AGENTS.md](AGENTS.md) first. It contains the full operating manual, file contracts, Genie API notes, and task runbooks.
