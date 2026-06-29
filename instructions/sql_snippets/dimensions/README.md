# Dimension Helpers — Repo-Only Layer

This directory is a repo-only helper layer for reusable SELECT expressions.
Dimension helpers are NOT deployed to the Genie room API.

They provide:
- Period boundary expressions (week_start, month_start, etc.)
- Grain labels
- Explanation helpers

## Format

Same as regular snippets: `id`, `alias`, `display_name`, `sql`, `instruction`.

## IMPORTANT

Dimension helper files appear here but should NOT be added to `instruction_library/activation/dimensions.active.yml`
if you want them to remain repo-only. They are available to be referenced by example_sql files.
