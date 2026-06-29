# 06 Change Guide for Agents

This is the implementation playbook for coding agents working on the Action Plans pipeline.
Read this file before making any changes.

## Files to Read First

When the task touches retrieval or playbooks:
- `setup/vector_search.py`
- `pipeline_playbook_generator/config/playbook_blueprint.yml`
- `pipeline_config.yml → playbooks.sources`

When the task touches trend analysis or Genie questions:
- `pipeline/trends_analysis.py`
- `pipeline_config.yml → questions.seeds`

When the task touches action plan generation or LLM prompts:
- `pipeline/action_plans.py`
- `pipeline_config.yml → system_prompts`

When the task touches workflow scheduling:
- `setup/create_workflow.py`
- `pipeline_config.yml → workflow`

When the task touches the playbook content itself:
- `pipeline_playbook_generator/config/playbook_blueprint.yml`
- then re-run `generate_playbook.py` and re-upload/re-index

---

## Stable Cross-Notebook Contract

Treat these as one contract. Changing any one in isolation makes the pipeline logically inconsistent:

- `question_category` values
- `playbooks.sources` registry entries in `pipeline_config.yml`
- `questions.seeds` entries in `pipeline_config.yml`
- `system_prompts` keys in `pipeline_config.yml`
- The `question_category` column in the playbook chunks table and VS index

---

## Recipe: Add a New Domain

1. Add domain content to `pipeline_playbook_generator/config/playbook_blueprint.yml`:
   - New key under `domains:` matching a `metadata/columns/*.yml` filename
   - Fill in `kpis_covered`, `scenarios`, `action_cards`, `example_plans`

2. Re-run the generator (local machine):
   ```
   python pipeline_playbook_generator/generate_playbook.py --kit-format genie_kit
   ```

3. Upload the new PDF (if `source_type: volume`):
   ```
   python setup/upload_pdfs.py
   ```

4. In `pipeline/pipeline_config.yml`, add matching entries in ALL THREE of:
   - `playbooks.sources` — new `{pdf_file, question_category}`
   - `questions.seeds` — new `{category, question}`
   - `system_prompts` — new key with the expert prompt for this domain

5. Re-run `setup/vector_search.py` in Databricks to chunk and index the new PDF.

6. Run `pipeline/trends_analysis.py` manually to validate Genie responds correctly.

7. Run `pipeline/action_plans.py` manually to validate retrieval and LLM output.

8. Only update the workflow schedule after the end-to-end test passes.

---

## Recipe: Change a Seed Question

1. Edit the question text in `pipeline_config.yml → questions.seeds`.
2. Re-run `pipeline/trends_analysis.py` — the MERGE will update the existing row.
3. Keep the `category` value unchanged unless you are also updating the PDF registry and prompt.

---

## Recipe: Update an LLM System Prompt

1. Edit the prompt in `pipeline_config.yml → system_prompts[category]`.
2. The change takes effect on the next run of `pipeline/action_plans.py` — no notebook edit required.
3. Keep the three output sections stable unless downstream consumers also change:
   - `Immediate Actions (next 24-48 hours)`
   - `Short-term Actions (1-2 weeks)`
   - `Measurement Targets`

---

## Recipe: Change a Config Value (catalog, schema, endpoint, etc.)

1. Edit only `pipeline/pipeline_config.yml`.
2. If changing catalog/schema/table_prefix: re-run `setup/vector_search.py` to recreate objects in the new location.
3. If changing VS endpoint: re-run `setup/vector_search.py` to create the index on the new endpoint.
4. If changing LLM endpoint: no setup needed — takes effect on the next action_plans run.
5. Do not rename a `question_category` in only `pipeline_config.yml` — the VS index still filters on the old value until re-indexed.

---

## Recipe: Regenerate and Re-Index Playbooks

Use this when playbook content (scenarios, action cards, example plans) has changed:

1. Edit `pipeline_playbook_generator/config/playbook_blueprint.yml`.
2. Run `generate_playbook.py` locally.
3. Run `upload_pdfs.py` (if using volume source).
4. Run `setup/vector_search.py` in Databricks — the MERGE will update existing chunk rows.
5. VS index sync is triggered automatically.

---

## Do-Not-Break Rules

- Do not hardcode catalog names, table names, or endpoint names in any notebook.
- Do not change a `question_category` value in only one place.
- Do not change playbook heading patterns without checking that chunk extraction still works.
- Do not assume the live Delta tables match the current `pipeline_config.yml` seeds — they may contain historical rows.
- Do not run `setup/create_workflow.py` without reviewing the cluster node type for your workspace.
- Do not delete or truncate the playbook chunks table without re-running vector-search setup immediately after.

---

## Validation Checklist

Before closing any change, confirm:

- [ ] `pipeline_config.yml` has no `{{PLACEHOLDER}}` values remaining
- [ ] Every category in `questions.seeds` has a matching entry in `playbooks.sources`
- [ ] Every category in `playbooks.sources` has a matching entry in `system_prompts`
- [ ] `{prefix}_playbook_chunks` has rows for every active category
- [ ] The Vector Search index is ONLINE and synced
- [ ] A manual run of `trends_analysis.py` completes without error
- [ ] A manual run of `action_plans.py` writes rows to `{prefix}_action_plan`
