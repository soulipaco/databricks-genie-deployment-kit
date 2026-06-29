# Skill: pipeline_add_domain

## Trigger
- "add a domain to the pipeline"
- "add a new question category"
- "add a playbook for X"
- "add a new domain"
- "pipeline add domain"

## Purpose

Add a new analysis domain (question category) to the Action Plans pipeline end-to-end.

A domain is the unit of analysis — e.g. `sales_performance`, `support_quality`, `customer_retention`.
Each domain requires exactly **4 coordinated changes** across 2 files. Missing any one causes
silent retrieval failures at runtime — this skill ensures all 4 are always added together.

The 4 changes that must stay in sync:
1. New domain block in `pipeline_playbook_generator/config/playbook_blueprint.yml`
2. New entry in `pipeline_config.yml → playbooks.sources`
3. New entry in `pipeline_config.yml → questions.seeds`
4. New entry in `pipeline_config.yml → system_prompts`

**Prerequisite:** `pipeline_configure` must be complete (zero `{{PLACEHOLDER}}` values).

## Inputs

| Input | Source | Required | Notes |
|---|---|---|---|
| `domain_key` | User | Yes | Snake_case key — must partially match a `metadata/columns/*.yml` filename |
| `display_name` | User | Yes | Human-readable name, e.g. `"RCA Detractor Analysis"` |
| `question_category` | User | Yes | Usually same as `domain_key`. Used for VS filter and config keys |
| `pdf_filename` | User | No | Default: `"{table_prefix}_{domain_key}_action_playbook.pdf"` |
| `seed_question` | User | Yes | The Deep Research question text (1-3 sentences, specific to the domain KPIs) |
| `system_prompt` | User | Yes | LLM expert persona and output instructions for this domain |
| `kpis` | User | Yes | List of KPI names + descriptions |
| `scenarios` | User | Yes | At least 1 scenario with symptoms, causes, actions, measurement targets |
| `action_cards` | User | No | Short retrieval snippets (recommended: 1 per scenario) |
| `example_plans` | User | No | 1-2 worked examples |

## Steps

### Step 1 — Validate the domain key

Read `metadata/columns/` and find all `.yml` filenames.
Confirm that `domain_key` partially matches at least one filename stem.

If no match: warn the user that the generator may fail to find the column metadata,
and ask whether to proceed anyway or use a different key.

Check `pipeline_config.yml → playbooks.sources` — if `question_category` already exists,
confirm with the user whether they want to update an existing domain or add a new one.
If updating existing content, redirect to skill `pipeline_update_playbook` instead.

### Step 2 — Add domain block to `playbook_blueprint.yml`

Read `pipeline_playbook_generator/config/playbook_blueprint.yml`.

Append a new domain under the `domains:` key:

```yaml
domains:
  <domain_key>:
    display_name: "<display_name>"
    question_category: "<question_category>"

    playbook_title: "<display_name> Operations Playbook"
    playbook_subtitle: "Action Plan Recommendations for KPI-Driven Trend Analysis"
    playbook_note: >-
      Generated from this deployment kit. SME review recommended before production use.
    intro_text: >-
      <brief intro — 1-2 sentences about the domain and what this playbook covers>

    kpis_covered:
      - name: "<kpi_1_name>"
        description: "<kpi_1_description>"
      # repeat for all KPIs

    interpretation_rules:
      - "<rule_1>"
      - "<rule_2>"

    scenarios:
      - letter: "A"
        title: "<scenario_a_title>"
        symptoms:
          - "<symptom_1>"
        likely_causes:
          - "<cause_1>"
        action_plan_recommendations:
          - heading: "Immediate actions (today-48h)"
            actions:
              - "<action_1>"
          - heading: "Short-term actions (1-4 weeks)"
            actions:
              - "<action_1>"
        measurement_targets:
          - "<target_1>"

    action_cards:
      - title: "<card_title>"
        trigger: "<trigger_condition>"
        actions:
          - "<action_1>"
        expected_impact: "<expected_impact>"

    example_plans:
      - number: 1
        title: "<example_title>"
        observed_trend: "<observed_trend_description>"
        plan:
          - "<plan_step_1>"
        success_metrics: "<success_metrics>"
```

### Step 3 — Add 3 entries to `pipeline_config.yml`

Read `pipeline/pipeline_config.yml` and add entries in exactly these three sections:

**3a. Under `playbooks.sources`:**
```yaml
playbooks:
  sources:
    - pdf_file: "<pdf_filename>"
      question_category: "<question_category>"
```

**3b. Under `questions.seeds`:**
```yaml
questions:
  seeds:
    - category: "<question_category>"
      question: >-
        <seed_question>
```

**3c. Under `system_prompts`:**
```yaml
system_prompts:
  <question_category>: |
    <system_prompt>
```

**Critical:** All three keys (`pdf_file`/category, seed category, system_prompt key) must use
the SAME `question_category` value. Verify this before saving.

### Step 4 — Validate the cross-notebook contract

After writing both files, verify:
- `question_category` appears in `playbooks.sources` ✓
- Same `question_category` appears in `questions.seeds` ✓
- Same `question_category` appears as a key in `system_prompts` ✓
- Domain key in `playbook_blueprint.yml` partially matches a file in `metadata/columns/` ✓

If any check fails, fix it before proceeding.

### Step 5 — Generate PDFs (local machine)

```bash
python pipeline_playbook_generator/generate_playbook.py --kit-format genie_kit
```

Confirm the new PDF appears in `pipeline_playbook_generator/generated/pdfs/`.

If the generator fails with a "domain not found" error, the domain key does not match
any `metadata/columns/*.yml` filename — revisit Step 1.

### Step 6 — Upload new PDF (if source_type: volume)

```bash
python setup/upload_pdfs.py
```

If `source_type: local`, skip this step.

### Step 7 — Re-index Vector Search (Databricks — instruct user)

The VS index must be refreshed to include the new domain's chunks.

Instruct the user:
> In Databricks, open `setup/vector_search.py` and run it. It will MERGE the new
> PDF chunks into `{prefix}_playbook_chunks` and sync the index automatically.

After re-indexing, validate:
```sql
SELECT question_category, COUNT(*) AS chunk_count
FROM {catalog}.{schema}.{table_prefix}_playbook_chunks
GROUP BY question_category
ORDER BY question_category;
```
The new `question_category` must appear in the result.

### Step 8 — Report to user

Summarize what was added:
- Domain key and question_category
- PDF filename generated
- The 3 `pipeline_config.yml` entries added
- Next step: re-run `setup/vector_search.py` (if not yet done)

## Outputs

- Updated `pipeline_playbook_generator/config/playbook_blueprint.yml` — new domain block
- Updated `pipeline/pipeline_config.yml` — 3 new entries (sources, seeds, system_prompts)
- New `pipeline_playbook_generator/generated/pdfs/<pdf_filename>` — generated PDF
- UC Volume (if `source_type: volume`) — PDF uploaded

## Validation

- [ ] `playbook_blueprint.yml` has new domain under `domains:` key
- [ ] `pipeline_config.yml → playbooks.sources` has new `{pdf_file, question_category}` entry
- [ ] `pipeline_config.yml → questions.seeds` has new `{category, question}` entry
- [ ] `pipeline_config.yml → system_prompts` has new key matching `question_category`
- [ ] All three `question_category` values are identical
- [ ] New PDF exists in `generated/pdfs/`
- [ ] `{prefix}_playbook_chunks` has rows for the new category after re-indexing

## References

- `pipeline/docs/03_playbook_ingestion_and_chunking.md` — Chunking rules and PDF structure
- `pipeline/docs/06_change_guide_for_agents.md` — Cross-notebook contract rules
- `pipeline/pipeline_config.yml` — File to update
- `pipeline_playbook_generator/config/playbook_blueprint.yml` — File to update
- `pipeline_playbook_generator/README.md` — Generator usage
