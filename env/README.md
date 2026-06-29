# Environment Configuration

This directory contains environment-specific configuration files.

## Files

| File | Purpose |
|------|---------|
| `local.yml` | Local development environment |
| `prod.yml` | Production environment |

## How to Use

The push/pull scripts read from `env/<environment>.yml`:

```bash
# Deploy using local config
python scripts/push_folder_to_room.py --env local

# Deploy using prod config
python scripts/push_folder_to_room.py --env prod
```

## What Goes Here

- `workspace_url` — Databricks workspace URL
- `warehouse_id` — SQL warehouse ID for executing queries
- `space_id` — Genie space ID (null for new rooms)
- `parent_path` — Workspace folder path where the room lives

## Security

**NEVER commit real credentials to version control.**

Options for managing credentials:
- Add `env/*.local.yml` to `.gitignore` and store personal values there
- Use environment variables: `DATABRICKS_HOST`, `DATABRICKS_TOKEN`
- Use a secrets manager (Azure Key Vault, AWS Secrets Manager, etc.)
- In CI/CD: inject values from your pipeline secret store
