# Action Plans Pipeline — Docs

This folder documents the action plans pipeline so future agents and maintainers
can change it safely without requiring manual context injection.

## Recommended reading order

1. [01_system_overview.md](01_system_overview.md)
2. [02_object_map.md](02_object_map.md)
3. [03_playbook_ingestion_and_chunking.md](03_playbook_ingestion_and_chunking.md)
4. [04_pipeline_behavior.md](04_pipeline_behavior.md)
5. [05_runbook.md](05_runbook.md)
6. [06_change_guide_for_agents.md](06_change_guide_for_agents.md)

## Source of truth

All Databricks object names, endpoint references, and configurable values live in
one place only:

```
pipeline/pipeline_config.yml
```

The notebooks contain no hardcoded paths. If code and docs drift, update docs in
the same change set.
