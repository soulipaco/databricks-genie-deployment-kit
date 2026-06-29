# Skill: pipeline_setup

## Trigger
- "set up the pipeline"
- "initialize the action plans pipeline"
- "first-time pipeline setup"
- "run pipeline setup"
- "pipeline setup"

## Purpose

Orchestrate the full first-time setup sequence for the Action Plans pipeline.
Each step has a hard dependency on the previous one — this skill enforces the correct order
and checks each step before advancing.

**Prerequisite:** `pipeline_configure` must be complete (zero `{{PLACEHOLDER}}` values).

## Inputs

| Input | Source | Required | Notes |
|---|---|---|---|
| `kit_root` | Auto | Yes | Repo root — resolved as parent of `pipeline/` |
| `source_type` | Config | Yes | Read from `pipeline/pipeline_config.yml → playbooks.source_type` |

No additional inputs from the user — all values come from `pipeline_config.yml`.

## Steps

### Step 0 — Verify config is clean

Read `pipeline/pipeline_config.yml` and scan for any `{{...}}` pattern.

If any placeholders remain:
- List all unconfigured fields
- Stop and tell the user to run `pipeline_configure` first

If config is clean, proceed.

### Step 1 — Generate playbook PDFs (local machine)

Run from the repo root:
```bash
python pipeline_playbook_generator/generate_playbook.py --kit-format genie_kit
```

Expected output in `pipeline_playbook_generator/generated/pdfs/`:
- One PDF file per entry in `pipeline_config.yml → playbooks.sources`

Verify each PDF listed under `playbooks.sources[].pdf_file` exists in the output directory.
If any PDF is missing, check `config/playbook_blueprint.yml` — the domain key must partially
match a filename in `metadata/columns/`.

### Step 2 — Upload PDFs to UC Volume (only if source_type: volume)

If `playbooks.source_type == "volume"`:
```bash
# Dry-run first to verify paths
python setup/upload_pdfs.py --dry-run

# Then upload for real
python setup/upload_pdfs.py
```

If `playbooks.source_type == "local"`, skip this step — the notebooks read PDFs directly
from the workspace repo path.

Verify: the dry-run output lists every PDF file with the correct target Volume path.

### Step 3 — Run Vector Search setup (Databricks)

This step must be run INSIDE Databricks (it uses `dbutils` and the VS SDK).

Instruct the user:
> Open Databricks → Repos → navigate to this repo → open `setup/vector_search.py` → Run All.

What it does:
- Creates `{prefix}_playbook_chunks` table with Change Data Feed enabled
- Chunks every PDF source and MERGEs rows into the table
- Creates or syncs the `{prefix}_playbook_chunks_index` Vector Search index

After running, validate in Databricks SQL:
```sql
SELECT question_category, COUNT(*) AS chunk_count
FROM {catalog}.{schema}.{table_prefix}_playbook_chunks
GROUP BY question_category
ORDER BY question_category;
```
Every category in `playbooks.sources` must appear in the result with chunk_count > 0.

Also confirm the VS index status is **ONLINE** (not PROVISIONING) in Databricks → Vector Search
before proceeding to Step 4.

### Step 4 — Create the Databricks workflow (Databricks)

This step must be run INSIDE Databricks.

Instruct the user:
> Open Databricks → Repos → navigate to this repo → open `setup/create_workflow.py` → Run All.

What it does:
- Finds or creates a workflow job named `workflow.name` from config
- Schedules two tasks in sequence: `trends_analysis → action_plans`
- Uses the cron schedule and timezone from config

Note the returned `job_id` for future reference.

Verify in Databricks → Workflows that the job exists and both tasks are listed.

**Before enabling the schedule**, review the cluster configuration in `setup/create_workflow.py`
(node type, Spark version) and confirm it matches your workspace's available instance types.

### Step 5 — Run a manual end-to-end test (Databricks)

Run `pipeline/trends_analysis.py` manually first:
> Open Databricks → Repos → open `pipeline/trends_analysis.py` → Run All.

Validate:
```sql
SELECT question_category, warning, LEFT(summary, 150) AS preview
FROM {catalog}.{schema}.{table_prefix}_trends_analysis
ORDER BY timestamp DESC
LIMIT 10;
```

Then run `pipeline/action_plans.py`:
> Open `pipeline/action_plans.py` → Run All.

Validate:
```sql
SELECT question_category, LEFT(action_plan, 200) AS plan_preview, timestamp
FROM {catalog}.{schema}.{table_prefix}_action_plan
ORDER BY timestamp DESC
LIMIT 5;
```

### Step 6 — Enable the schedule

Once the manual test passes, enable the workflow schedule in Databricks → Workflows.

## Outputs

- `pipeline_playbook_generator/generated/pdfs/*.pdf` — Generated playbook PDFs
- UC Volume (if `source_type: volume`) — PDFs uploaded
- `{prefix}_playbook_chunks` Delta table — Chunks indexed
- `{prefix}_playbook_chunks_index` VS index — ONLINE
- Databricks workflow job — Created and scheduled

## Validation

- [ ] Zero `{{PLACEHOLDER}}` values in `pipeline/pipeline_config.yml`
- [ ] One PDF exists per `playbooks.sources` entry in `generated/pdfs/`
- [ ] `{prefix}_playbook_chunks` has rows for every `question_category` in `playbooks.sources`
- [ ] VS index status is ONLINE
- [ ] Databricks workflow job exists with both tasks listed
- [ ] Manual runs of `trends_analysis.py` and `action_plans.py` complete without error
- [ ] `{prefix}_trends_analysis` and `{prefix}_action_plan` tables have rows

## References

- `pipeline/docs/01_system_overview.md` — End-to-end flow
- `pipeline/docs/05_runbook.md` — Detailed setup sequence with validation SQL
- `pipeline/pipeline_config.yml` — Single source of truth
- `setup/vector_search.py` — VS setup notebook
- `setup/create_workflow.py` — Workflow creation notebook
- `setup/upload_pdfs.py` — PDF upload helper
