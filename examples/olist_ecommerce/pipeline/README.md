# Olist Action-Plan Pipeline Example

This folder adapts the generic `pipeline/` and `pipeline_playbook_generator/` framework for the Olist E-Commerce demo.

The goal is to show a complete analytics-agent workflow:

1. Genie Deep Research detects operational trends and warning patterns.
2. A generated Olist action playbook is chunked and indexed with Databricks Vector Search.
3. Retrieved playbook context is passed to an LLM endpoint.
4. The pipeline writes prioritized action plans to Delta tables for dashboarding or review.

For the production operating pattern, see [PRODUCTION_PLAYBOOK.md](PRODUCTION_PLAYBOOK.md).

## Config Files

- `pipeline_config.yml` configures the runtime pipeline for this demo.
- `../pipeline_playbook_generator/config/playbook_blueprint.yml` defines the Olist action playbook content.
- `PRODUCTION_PLAYBOOK.md` explains how this pattern can be governed in a real analytics environment.

## Required Workspace Values

Before running the action-plan pipeline, replace:

- `{{VS_ENDPOINT_NAME}}`
- `{{LLM_ENDPOINT_NAME}}`

The rest of the demo is already aligned to:

- Genie Space ID: `01f173e821ef1c70960778c4ea3ced3a`
- Catalog: `workspace`
- Schema: `olist_ecommerce`
- Table prefix: `olist_ops`
- Playbook PDF source: local generated PDF path

## Run Order

From the repo root:

```bash
python pipeline_playbook_generator/generate_playbook.py ^
  --kit-root examples/olist_ecommerce ^
  --config examples/olist_ecommerce/pipeline_playbook_generator/config/playbook_blueprint.yml ^
  --output-dir examples/olist_ecommerce/pipeline_playbook_generator/generated
```

Then in Databricks, copy or adapt:

- `setup/vector_search.py`
- `pipeline/trends_analysis.py`
- `pipeline/action_plans.py`

Use this folder's `pipeline_config.yml` as the config source.

## Production Use

In a production workspace, the playbook should become reviewed operational content:

- generate playbook markdown and PDF from Git-reviewed metadata
- upload reviewed PDFs to a Unity Catalog Volume
- index chunks in Databricks Vector Search
- retrieve scenario-specific guidance when Genie identifies a metric movement
- send the trend summary and retrieved context to a governed LLM endpoint
- write the resulting action plan to a Delta table with reviewer status and lineage

## Seed Analysis Question

The pipeline is seeded with a single broad Deep Research question:

> Analyze Olist e-commerce operations performance across order value, late delivery, review score, Pareto category concentration, customer-state concentration, and target gaps for reaching a 4.2 average review score. Identify warning areas that need action.
