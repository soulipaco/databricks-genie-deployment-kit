# Skill: pipeline_configure

## Trigger
- "configure the pipeline"
- "set up pipeline_config.yml"
- "fill in the pipeline config"
- "configure action plans"
- "pipeline config"

## Purpose

Fill in every `{{PLACEHOLDER}}` in `pipeline/pipeline_config.yml` so the pipeline
notebooks can start. Every notebook refuses to run until this is complete.

Run this skill FIRST — before `pipeline_setup`, `pipeline_add_domain`, or any notebook.

## Inputs

| Input | Source | Required | Notes |
|---|---|---|---|
| `space_id` | User | Yes | Genie space ID — from `room.config.yml` or the Databricks Genie UI URL |
| `catalog_name` | User | Yes | Unity Catalog catalog where pipeline tables will be created |
| `schema_name` | User | Yes | Schema (database) within that catalog |
| `table_prefix` | User | Yes | Prefix for all Delta tables — usually derived from `room_name` in `room.config.yml` |
| `vs_endpoint` | User | Yes | Vector Search endpoint name — visible in Databricks → Vector Search |
| `llm_endpoint` | User | Yes | LLM serving endpoint name — visible in Databricks → Serving |
| `source_type` | User | Yes | `"volume"` (production) or `"local"` (quick iteration without a Volume) |
| `volume_path` | User | If `source_type: volume` | UC Volume path: `/Volumes/catalog/schema/volume_name` |
| `workflow_name` | User | No | Default: `"{table_prefix} — Action Plans"` |
| `schedule_cron` | User | No | Quartz cron expression. Default: `"0 0 7 * * ?"` (07:00 UTC daily) |
| `timezone` | User | No | Default: `"UTC"` |

## Steps

1. **Read `pipeline/pipeline_config.yml`** — Note every `{{PLACEHOLDER}}` currently present.

2. **Collect inputs** — Ask the user for each required value listed above.
   For `table_prefix`: if not provided, read `room_name` from `room.config.yml` and propose
   `{room_name}` as the prefix.
   For `space_id`: if not provided, read it from `room.config.yml → space_id`.

3. **Validate inputs before writing:**
   - `space_id` must be a non-empty string (typically 32 hex chars)
   - `catalog_name`, `schema_name` must be non-empty, no spaces
   - `table_prefix` must be non-empty, no spaces, no dots
   - `vs_endpoint` and `llm_endpoint` must be non-empty strings
   - `source_type` must be exactly `"volume"` or `"local"`
   - If `source_type: volume`, `volume_path` must start with `/Volumes/`

4. **Write `pipeline/pipeline_config.yml`** — Replace each placeholder with the collected value.
   Key replacements:
   ```yaml
   genie:
     space_id: "<space_id>"

   catalog:
     name: "<catalog_name>"
     schema: "<schema_name>"
     table_prefix: "<table_prefix>"

   vector_search:
     endpoint: "<vs_endpoint>"

   llm:
     endpoint: "<llm_endpoint>"

   playbooks:
     source_type: "<source_type>"
     volume_path: "<volume_path>"       # only if source_type: volume

   workflow:
     name: "<workflow_name>"
     schedule_cron: "<schedule_cron>"
     timezone: "<timezone>"
   ```
   Do NOT change the `questions.seeds` or `system_prompts` sections — those are managed
   by `pipeline_add_domain`.

5. **Verify zero placeholders** — Scan the written file for any remaining `{{...}}` pattern.
   If any are found, list them and ask the user for the missing values before finishing.

6. **Report to user** — Confirm which values were set and list the next step:
   - If this is first-time setup: run skill `pipeline_setup`
   - If adding a new domain: run skill `pipeline_add_domain`

## Outputs

- `pipeline/pipeline_config.yml` — All infrastructure placeholders filled in

## Validation

- [ ] `pipeline/pipeline_config.yml` contains zero `{{PLACEHOLDER}}` strings
- [ ] `genie.space_id` matches the `space_id` field in `room.config.yml` (if the room is already configured)
- [ ] `catalog.table_prefix` does not contain spaces or dots
- [ ] If `source_type: volume`, `playbooks.volume_path` starts with `/Volumes/`
- [ ] `playbooks.sources`, `questions.seeds`, and `system_prompts` are present and non-empty
  (they may still have placeholder content if no domain has been configured yet — that is normal
  until `pipeline_add_domain` is run)

## References

- `pipeline/pipeline_config.yml` — File to edit
- `room.config.yml` — Source of `space_id` and `room_name`
- `pipeline/docs/01_system_overview.md` — Pipeline overview
- `pipeline/docs/02_object_map.md` — Table naming conventions
- `pipeline/docs/06_change_guide_for_agents.md` — Config change rules
