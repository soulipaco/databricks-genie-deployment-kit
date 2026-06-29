# Column Metadata

This directory contains per-table column configuration files.

## File Naming
`<table_name>.yml` — One file per table registered in `data_sources/tables.yml`.

## Format
See `templates/column_metadata.yml` for the template.

## Required
Every table in `data_sources/tables.yml` MUST have a matching file here.

## How Column Config Affects Genie

| Field | Effect |
|-------|--------|
| `exclude: true` | Column is completely hidden from Genie |
| `enable_entity_matching: true` | Genie can fuzzy-match entity names |
| `get_example_values: true` | Genie fetches sample values for context |
| `build_value_dictionary: true` | Genie builds a lookup dictionary |
| `enable_format_assistance: true` | Genie helps with data formatting |
