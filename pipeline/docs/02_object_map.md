# 02 Object Map

## Single Source of Truth

All Databricks object names are derived from `pipeline/pipeline_config.yml`.
No notebook contains hardcoded catalog names, schema names, or table names.

## Naming Pattern

Every Delta table follows this pattern:

```
{catalog.name}.{catalog.schema}.{catalog.table_prefix}_{suffix}
```

| Suffix | Purpose |
|---|---|
| `trends_questions` | Active seed questions per category |
| `trends_analysis` | Genie Deep Research results |
| `action_plan` | LLM-generated action plans |
| `playbook_chunks` | PDF text chunks for Vector Search (CDF enabled) |
| `playbook_chunks_index` | Databricks Vector Search index |

## Example

With `pipeline_config.yml`:
```yaml
catalog:
  name: my_catalog
  schema: my_schema
  table_prefix: demo_room
```

The resulting objects are:

| Purpose | Object |
|---|---|
| Trends questions | `my_catalog.my_schema.demo_room_trends_questions` |
| Trends analysis | `my_catalog.my_schema.demo_room_trends_analysis` |
| Action plans | `my_catalog.my_schema.demo_room_action_plan` |
| Playbook chunks | `my_catalog.my_schema.demo_room_playbook_chunks` |
| Playbook chunk index | `my_catalog.my_schema.demo_room_playbook_chunks_index` |

## Other Configurable Objects

| Object | Config key |
|---|---|
| Genie space | `genie.space_id` |
| Vector Search endpoint | `vector_search.endpoint` |
| Embedding model | `vector_search.embedding_model` |
| LLM endpoint | `llm.endpoint` |
| PDF UC Volume path | `playbooks.volume_path` |
| PDF local path | `playbooks.local_path` |
| Workflow name | `workflow.name` |
| Workflow schedule | `workflow.schedule_cron` |

## Stability Rules

- Do not hardcode any object name in a notebook — always derive from config.
- If a table or index name needs to change, change only `pipeline_config.yml` and re-run setup notebooks.
- The Vector Search index requires `delta.enableChangeDataFeed = true` on the source table — this is set automatically by `setup/vector_search.py`.
- Never point the test variant of this kit at production tables from a different kit.
