# room.config.tpl — Annotated Room Config Scaffold
# This is a fully annotated template for configuring a new Genie Room.
# Replace all {{PLACEHOLDER}} values.

# ── Identity ───────────────────────────────────────────────────
# room_name: used in API calls and internal references (no spaces)
# title: shown in Databricks UI
# description: shown in Databricks UI, markdown supported
room_name: {{ROOM_NAME}}
title: {{ROOM_DISPLAY_TITLE}}
description: |-
  {{ROOM_DESCRIPTION}}

  Supported analysis includes:
  - {{CAPABILITY_1}}
  - {{CAPABILITY_2}}
  - {{CAPABILITY_3}}

version: 2
purpose: {{PURPOSE_NOTE}}
source_of_truth: repo
parent_path: {{WORKSPACE_PARENT_PATH}}

# ── Sample Questions ───────────────────────────────────────────
# Shown in the Genie room UI as conversation starters
# Generate IDs: python -c "import uuid; print(uuid.uuid4().hex)"
sample_questions:
  - id: {{SQ_ID_1}}
    question: {{SAMPLE_Q_1}}
  - id: {{SQ_ID_2}}
    question: {{SAMPLE_Q_2}}
  - id: {{SQ_ID_3}}
    question: {{SAMPLE_Q_3}}
  - id: {{SQ_ID_4}}
    question: {{SAMPLE_Q_4}}
  - id: {{SQ_ID_5}}
    question: {{SAMPLE_Q_5}}

# ── Data Sources ───────────────────────────────────────────────
# Paths to table and column config files
data_sources: data_sources/tables.yml
column_metadata: metadata/columns/

# ── Instructions ───────────────────────────────────────────────
# Deploy surface (materialized from instruction_library/)
instructions:
  general: instructions/general.md
  example_sql: instructions/example_sql/
  sql_snippets:
    filters: instructions/sql_snippets/filters/
    measures: instructions/sql_snippets/measures/
    dimensions: instructions/sql_snippets/dimensions/

# ── Benchmarks ─────────────────────────────────────────────────
benchmarks: benchmarks/

# ── Bootstrap Reference ────────────────────────────────────────
bootstrap_snapshot: snapshots/exported_space.json

# ── Notes ──────────────────────────────────────────────────────
# - Environment values (workspace URL, warehouse ID, space ID) go in env/*.yml
# - Capacity limits go in instruction_library/activation/limits.yml
# - See AGENTS.md for full kit structure and operational procedures
