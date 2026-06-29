# Databricks notebook source
# MAGIC %pip install databricks-sdk pyyaml --quiet
# MAGIC

# COMMAND ----------

# ============================================================================
# Setup: Create Databricks Workflow
# ============================================================================
# Run ONCE to create the action plans workflow. Re-running is safe — it
# detects an existing workflow by name and updates it in place.
#
# The workflow runs two notebooks in sequence:
#   1. pipeline/trends_analysis.py   — Genie Deep Research → Delta table
#   2. pipeline/action_plans.py      — VS RAG + LLM → action_plan Delta table
#
# All parameters (schedule, cluster, timeout) come from pipeline_config.yml.
# The repo root is resolved dynamically — no hardcoded workspace paths.
# ============================================================================

# COMMAND ----------

import os
import re
import yaml

def _resolve_repo_root() -> str:
    try:
        nb_path = (
            dbutils.notebook.entry_point
            .getDbutils().notebook().getContext()
            .notebookPath().get()
        )
    except Exception:
        raise RuntimeError("This notebook must be run inside Databricks.")
    repo_root = os.path.dirname(os.path.dirname(nb_path))
    if not repo_root.startswith("/Workspace"):
        repo_root = "/Workspace" + repo_root
    return repo_root


def _find_placeholders(obj, path="") -> list:
    found = []
    if isinstance(obj, str):
        for match in re.finditer(r"\{\{[^}]+\}\}", obj):
            found.append((path, match.group(0)))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            found.extend(_find_placeholders(v, path=f"{path}.{k}" if path else k))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            found.extend(_find_placeholders(item, path=f"{path}[{i}]"))
    return found


def load_config():
    repo_root = _resolve_repo_root()
    config_path = f"{repo_root}/pipeline/pipeline_config.yml"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"pipeline_config.yml not found at:\n  {config_path}\n\n"
            "Ensure this notebook runs from a Databricks Repo."
        )
    placeholders = _find_placeholders(cfg)
    if placeholders:
        lines = "\n".join(f"  • {path}: {value}" for path, value in placeholders)
        raise ValueError(
            f"pipeline_config.yml contains unconfigured placeholder(s):\n{lines}\n\n"
            f"Edit {config_path} and replace all {{{{PLACEHOLDER}}}} values before running."
        )
    return cfg, repo_root


CFG, REPO_ROOT = load_config()
print(f"Config loaded — repo root: {REPO_ROOT}")

WORKFLOW_NAME     = CFG["workflow"]["name"]
SCHEDULE_CRON     = CFG["workflow"]["schedule_cron"]
TIMEZONE          = CFG["workflow"].get("timezone", "UTC")
TRENDS_NB_PATH    = f"{REPO_ROOT}/pipeline/trends_analysis"
ACTION_PLANS_PATH = f"{REPO_ROOT}/pipeline/action_plans"

print(f"  Workflow name : {WORKFLOW_NAME}")
print(f"  Schedule      : {SCHEDULE_CRON} ({TIMEZONE})")
print(f"  Notebook 1    : {TRENDS_NB_PATH}")
print(f"  Notebook 2    : {ACTION_PLANS_PATH}")

# COMMAND ----------

# ============================================================================
# Build the workflow spec and create/update via SDK
# ============================================================================

from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs

w = WorkspaceClient()

WORKFLOW_SPEC = {
    "name": WORKFLOW_NAME,
    "schedule": {
        "quartz_cron_expression": SCHEDULE_CRON,
        "timezone_id": TIMEZONE,
        "pause_status": "UNPAUSED",
    },
    "max_concurrent_runs": 1,
    "tasks": [
        {
            "task_key": "trends_analysis",
            "notebook_task": {
                "notebook_path": TRENDS_NB_PATH,
                "source": "WORKSPACE",
            },
            "new_cluster": {
                "spark_version": "15.4.x-scala2.12",
                "node_type_id": "Standard_DS3_v2",
                "num_workers": 1,
                "spark_conf": {
                    "spark.databricks.cluster.profile": "singleNode",
                },
            },
            "timeout_seconds": 3600,
            "email_notifications": {},
        },
        {
            "task_key": "action_plans",
            "depends_on": [{"task_key": "trends_analysis"}],
            "notebook_task": {
                "notebook_path": ACTION_PLANS_PATH,
                "source": "WORKSPACE",
            },
            "new_cluster": {
                "spark_version": "15.4.x-scala2.12",
                "node_type_id": "Standard_DS3_v2",
                "num_workers": 1,
            },
            "timeout_seconds": 1800,
            "email_notifications": {},
        },
    ],
    "tags": {
        "pipeline": "action_plans",
        "kit": "genie_deployment_kit",
    },
}

# ── Find existing workflow by name ────────────────────────────────────────────
existing_job_id = None
for job in w.jobs.list(name=WORKFLOW_NAME):
    if job.settings.name == WORKFLOW_NAME:
        existing_job_id = job.job_id
        break

if existing_job_id:
    print(f"Workflow '{WORKFLOW_NAME}' already exists (job_id={existing_job_id}). Updating...")
    w.jobs.reset(job_id=existing_job_id, new_settings=jobs.JobSettings(**{
        k: v for k, v in WORKFLOW_SPEC.items() if k != "name"
    }))
    job_id = existing_job_id
    print(f"Workflow updated.")
else:
    print(f"Creating new workflow '{WORKFLOW_NAME}'...")
    created = w.jobs.create(**WORKFLOW_SPEC)
    job_id = created.job_id
    print(f"Workflow created — job_id={job_id}")

print(f"\nDone. Job ID: {job_id}")
print("Review and adjust the cluster configuration (node type, Spark version)")
print("to match your workspace's available instance types before running.")
