# 05 Runbook

## Prerequisites

Before running any notebook, `pipeline/pipeline_config.yml` must have all
`{{PLACEHOLDER}}` values filled in. Every notebook validates this at startup and
raises a `ValueError` listing every unconfigured field if any are found.

## First-Time Setup Sequence

### 1. Configure pipeline_config.yml

Edit `pipeline/pipeline_config.yml`. Minimum required fields:

```yaml
genie:
  space_id: "<your Genie space ID>"
catalog:
  name: "<your catalog>"
  schema: "<your schema>"
  table_prefix: "<your prefix>"
vector_search:
  endpoint: "<your VS endpoint name>"
llm:
  endpoint: "<your LLM endpoint name>"
playbooks:
  source_type: "volume"        # or "local"
  volume_path: "/Volumes/..."  # required if source_type: volume
```

### 2. Generate playbook PDFs (local machine)

```bash
python pipeline_playbook_generator/generate_playbook.py --kit-format genie_kit
```

Output: `pipeline_playbook_generator/generated/pdfs/*.pdf`

### 3. Upload PDFs to UC Volume (local machine, if source_type: volume)

```bash
python setup/upload_pdfs.py
# Dry-run first:
python setup/upload_pdfs.py --dry-run
```

### 4. Run vector-search setup (Databricks)

Run `setup/vector_search.py` in the Databricks workspace.

Validation:
```sql
SELECT question_category, COUNT(*) AS chunk_count
FROM {catalog}.{schema}.{table_prefix}_playbook_chunks
GROUP BY question_category
ORDER BY question_category;
```

Confirm the VS index exists and status is ONLINE before proceeding.

### 5. Create the workflow (Databricks)

Run `setup/create_workflow.py` once to create the scheduled job.
Note the returned `job_id` for future reference.

Adjust the cluster node type and Spark version in `create_workflow.py` to match
your workspace's available instance types before scheduling production runs.

### 6. Run trends analysis (Databricks)

Run `pipeline/trends_analysis.py` manually for the first test run.

Validation:
```sql
SELECT question_category, warning, LEFT(summary, 100) AS summary_preview
FROM {catalog}.{schema}.{table_prefix}_trends_analysis
ORDER BY timestamp DESC
LIMIT 20;
```

### 7. Run action plans (Databricks)

Run `pipeline/action_plans.py` manually after trends analysis completes.

Validation:
```sql
SELECT question_category, LEFT(action_plan, 200) AS plan_preview, timestamp
FROM {catalog}.{schema}.{table_prefix}_action_plan
ORDER BY timestamp DESC
LIMIT 10;
```

---

## Regular Operations

### Scheduled runs

The workflow created by `setup/create_workflow.py` runs both notebooks in sequence
on the configured cron schedule. No manual intervention is needed for routine runs.

### Refresh after playbook content changes

If you update `playbook_blueprint.yml` and regenerate PDFs:
1. Run `setup/upload_pdfs.py` (if using volume source).
2. Re-run `setup/vector_search.py` in Databricks to re-chunk and re-sync the index.
3. The next scheduled run picks up the updated chunks automatically.

### Add a new question category

See [06_change_guide_for_agents.md](06_change_guide_for_agents.md) — Recipe: Add a New Domain.

---

## Duplicate-Question Prevention

The seed question MERGE uses `(question_category, question)` as the natural key.
Re-running the notebook does not create duplicate rows. If legacy duplicates exist
from plain INSERT operations, clean them using:

```sql
-- Find duplicates
SELECT question_category, question, COUNT(*) AS row_count, MIN(id) AS first_id, MAX(id) AS last_id
FROM {catalog}.{schema}.{table_prefix}_trends_questions
GROUP BY question_category, question
HAVING COUNT(*) > 1;

-- Keep only the latest row per unique question (run carefully)
DELETE FROM {catalog}.{schema}.{table_prefix}_trends_questions
WHERE id NOT IN (
  SELECT MAX(id)
  FROM {catalog}.{schema}.{table_prefix}_trends_questions
  GROUP BY question_category, question
);
```

Always snapshot the table before destructive cleanup.
