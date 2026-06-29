# 01 System Overview

## Goal

The pipeline turns Genie trend analysis into concrete action plans by combining:

1. Playbook PDFs that encode domain expertise as structured scenarios and action cards
2. Semantic chunking of those PDFs into a Delta table
3. A Databricks Vector Search index over those chunks
4. Seeded trend-analysis questions sent to Genie Deep Research
5. Retrieved playbook context passed to an LLM for action-plan generation

## End-to-End Flow

```
playbook PDFs
    → setup/vector_search.py        (chunk + index)
    → pipeline/trends_analysis.py   (Genie Deep Research → Delta)
    → pipeline/action_plans.py      (VS retrieval + LLM → Delta)
```

### Step 1 — Ingest (setup/vector_search.py)

Reads one or more playbook PDFs (from UC Volume or workspace path, controlled by
`pipeline_config.yml → playbooks.source_type`), chunks the text, and writes rows
to `{prefix}_playbook_chunks`. Creates or syncs the Vector Search index on that table.

### Step 2 — Trends analysis (pipeline/trends_analysis.py)

1. Creates `{prefix}_trends_questions` and `{prefix}_trends_analysis` tables if absent.
2. Seeds active questions from `pipeline_config.yml → questions.seeds` via idempotent MERGE.
3. Sends each active question to Genie Deep Research using the configured space_id.
4. Parses Genie responses for `## Summary` and `## Warning` sections.
5. Appends results to `{prefix}_trends_analysis`.

### Step 3 — Action plans (pipeline/action_plans.py)

1. Reads today's latest trends-analysis rows.
2. For each row, retrieves matching playbook chunks from Vector Search filtered by `question_category`.
3. Selects the category-specific system prompt from `pipeline_config.yml → system_prompts`.
4. Calls the configured LLM endpoint.
5. Appends the generated action plan to `{prefix}_action_plan`.

## Folder Layout

```
pipeline/
  pipeline_config.yml          ← single source of truth for ALL parameters
  trends_analysis.py           ← Databricks notebook — step 2
  action_plans.py              ← Databricks notebook — step 3
  docs/                        ← this folder

setup/
  vector_search.py             ← Databricks notebook — step 1
  create_workflow.py           ← creates/updates the scheduled workflow job
  upload_pdfs.py               ← local helper — uploads PDFs to UC Volume

pipeline_playbook_generator/
  generate_playbook.py         ← local script — generates PDFs from kit metadata
  config/playbook_blueprint.yml ← domain content (scenarios, action cards, etc.)
  generated/pdfs/              ← generated PDFs ready to upload
```

## Stable Logical Contract

The cross-notebook contract is built around `question_category`.

Each category must stay aligned across all four layers:

| Layer | Location |
|---|---|
| PDF source registry | `pipeline_config.yml → playbooks.sources` |
| Seeded trend questions | `pipeline_config.yml → questions.seeds` |
| Category-specific LLM prompt | `pipeline_config.yml → system_prompts` |
| Vector Search filter | applied automatically using `question_category` column |

If one layer changes, all matching layers must change too.

## Fail-Fast Validation

Every notebook reads `pipeline_config.yml` at startup and immediately raises
`ValueError` if any `{{PLACEHOLDER}}` string is detected, listing every unconfigured
field by path. The pipeline will not advance past the config-loading cell until all
values are filled in.
