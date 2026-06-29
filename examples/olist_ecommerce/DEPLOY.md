# Deploy The Olist Genie Room

This example can deploy a Genie room directly from the files in `examples/olist_ecommerce`.

## Prerequisites

- Databricks SQL warehouse ID
- `DATABRICKS_HOST` environment variable
- `DATABRICKS_TOKEN` environment variable
- Gold table already created:
  - `workspace.olist_ecommerce.olist_order_metrics_mv`

## Dry Run

```powershell
$env:DATABRICKS_HOST="https://<workspace-host>"
$env:DATABRICKS_TOKEN="<token>"
python examples\olist_ecommerce\deploy_genie_room.py `
  --warehouse-id <warehouse-id> `
  --parent-path /Users/<your-email> `
  --dry-run
```

## Create Room

```powershell
python examples\olist_ecommerce\deploy_genie_room.py `
  --warehouse-id <warehouse-id> `
  --parent-path /Users/<your-email>
```

The script prints the new Genie Space ID after deployment.

## Update Existing Room

```powershell
python examples\olist_ecommerce\deploy_genie_room.py `
  --warehouse-id <warehouse-id> `
  --parent-path /Users/<your-email> `
  --space-id <existing-space-id>
```

## What Gets Deployed

- 1 data source table
- 5 sample questions
- 5 example SQL patterns
- 3 measure snippets
- 3 filter snippets
- 5 benchmark questions

