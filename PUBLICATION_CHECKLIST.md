# Publication Checklist

Use this before pushing the repository to GitHub or sharing it in a portfolio post.

## Repository Hygiene

- [ ] Run `python scripts/validate.py`.
- [ ] Run a secret scan:

```bash
rg -n "dapi|token|secret|password|dbc-|cloud.databricks.com|@[A-Za-z0-9._%+-]+" .
```

- [ ] Confirm raw datasets are not staged.
- [ ] Confirm generated build artifacts are not staged unless intentionally included.
- [ ] Confirm `.gitignore` is present.

## Olist Demo

- [ ] Confirm `examples/olist_ecommerce/DATASET.md` includes attribution.
- [ ] Confirm `examples/olist_ecommerce/SETUP_STATUS.md` reflects the latest deployed objects.
- [ ] Confirm `examples/olist_ecommerce/ENRICHMENT.md` explains the diagnostic tables.
- [ ] Confirm `examples/olist_ecommerce/DEPLOY.md` uses placeholders, not real tokens or personal workspace details.

## GitHub Readiness

- [ ] Choose a public-safe repository name, for example `databricks-genie-deployment-kit`.
- [ ] Add a license if you want others to reuse the code.
- [ ] Add screenshots only after checking they do not reveal tokens, private workspace URLs, or personal data.
- [ ] Rotate any Databricks token pasted into chat, shell history, or screenshots.

## Suggested Portfolio Story

This repository shows how to manage Databricks Genie as code:

- semantic metadata
- example SQL
- benchmark questions
- deployment automation
- AI/BI dashboard planning
- diagnostic enrichment for Pareto, driver-impact, and target-gap analysis

