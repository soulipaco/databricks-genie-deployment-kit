# 04 Pipeline Behavior

## trends_analysis.py

File: `pipeline/trends_analysis.py`

### What it does

1. Reads and validates `pipeline_config.yml` — fails fast if any placeholder is unconfigured.
2. Creates `{prefix}_trends_questions` and `{prefix}_trends_analysis` if they do not exist.
3. Builds the canonical seed set from `pipeline_config.yml → questions.seeds`.
4. Synchronizes seed questions with an idempotent MERGE (category + question as natural key).
5. Reads only active questions that match the current seed set.
6. Deduplicates by `question_category` and `question`, keeping the highest `id` per pair.
7. Sends each deduplicated question to Genie Deep Research using `genie.space_id`.
8. Parses Genie output into:
   - `response` — full Genie text
   - `summary` — extracted `## Summary` section
   - `warning` — extracted `## Warning` value (`0` or `1`)
9. Appends all results to `{prefix}_trends_analysis`.

### Why canonical deduplication matters

The table uses append-only writes. Re-runs or historical rows do not cause repeated
Genie calls — only rows matching the current seed set are processed, and only the
highest `id` per unique question is kept as the active row.

### Genie Deep Research client

The `DatabricksGenieClient` class handles:
- Authentication via Databricks SDK (falls back to env vars)
- Creating a Deep Research conversation
- Sending the question as a message
- Polling for completion (up to 15 minutes per question)
- Extracting the report summary from `attachments[].deep_research_report.report_summary`

The client uses the undocumented `/api/2.0/data-rooms/{space_id}/...` endpoints.
Do not change the `conversation_type: DEEP_RESEARCH` or `force_deep_research_planning: True`
fields — these are required for chain-of-thought KPI analysis.

### Response parsing

Both `extract_summary()` and `extract_warning()` use regex to locate the `## Summary`
and `## Warning` sections in the Genie response. The Genie space instructions
(in `resources/genie_space_instructions.txt`) enforce this structure.

If `## Warning` is absent or the value is not `0`/`1`, the raw `warning` field will
contain the issue description rather than a numeric flag.

---

## action_plans.py

File: `pipeline/action_plans.py`

### What it does

1. Reads and validates `pipeline_config.yml` — fails fast on any placeholder.
2. Creates `{prefix}_action_plan` if it does not exist.
3. Queries `{prefix}_trends_analysis` for today's latest row per `question_category`
   (grouped by category, MAX id for the current date).
4. For each row:
   a. Retrieves the top-N chunks from the Vector Search index, filtered by `question_category`.
   b. Selects the system prompt from `pipeline_config.yml → system_prompts[category]`.
   c. Builds a user message combining the trends summary and retrieved playbook excerpts.
   d. Calls the configured LLM endpoint via `mlflow.deployments`.
   e. Appends the generated action plan to `{prefix}_action_plan`.

### Retrieval query

The VS similarity search uses `"{category}: {trends_summary[:500]}"` as the query text
and filters by `question_category` so only relevant playbook chunks are retrieved.
`num_results` is controlled by `pipeline_config.yml → vector_search.num_results`.

### LLM output structure

The system prompt instructs the LLM to return three sections:
- `Immediate Actions (next 24-48 hours)`
- `Short-term Actions (1-2 weeks)`
- `Measurement Targets`

This structure is expected by the `{prefix}_action_plan` table consumers. Do not
change the section names without updating any downstream reports or dashboards.

### No Warning Filter In This Kit

This notebook processes all today's analysis rows regardless of warning value.
To use warning-only processing, add a filter on the `warning` column before
the for-loop.

---

## Category-Aware Prompting

System prompts are not hardcoded in notebooks — they live in `pipeline_config.yml`:

```yaml
system_prompts:
  sales_performance: |
    You are an expert sales performance analyst. ...
  another_category: |
    ...
```

If a category has no matching prompt, the notebook falls back to a generic expert prompt.
Always add an explicit prompt for each category — generic prompts produce weaker plans.

---

## Stable Runtime Contract

For the pipeline to work correctly, these must stay aligned:

| What | Where |
|---|---|
| Trend question categories | `pipeline_config.yml → questions.seeds[].category` |
| Playbook PDF categories | `pipeline_config.yml → playbooks.sources[].question_category` |
| System prompt keys | `pipeline_config.yml → system_prompts` keys |
| VS index filter field | `question_category` column in `{prefix}_playbook_chunks` |

If any of these drifts relative to the others, the pipeline will still run but will
produce empty or irrelevant retrieval results for the mismatched category.
