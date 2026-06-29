# Playbook Generator

Generates action plan PDFs from the deployment kit's metadata and geniecode context.
PDFs are used as the knowledge base for the Vector Search RAG pipeline.

## When to run

Run the generator whenever you:
- Add or update `metadata/columns/*.yml` files
- Edit `geniecode/DOMAIN_RULES.md` or `geniecode/KNOWLEDGE_BASE.md`
- Change scenarios, action cards, or example plans in `config/playbook_blueprint.yml`
- Onboard a new domain / question category

After regenerating, upload the PDFs and re-sync the Vector Search index:
```
python setup/upload_pdfs.py       # if source_type: volume
python setup/vector_search.py     # run in Databricks to re-index
```

## Quick start

```bash
# From the repo root:
pip install -r pipeline_playbook_generator/requirements.txt   # first time only
python pipeline_playbook_generator/generate_playbook.py --kit-format genie_kit
```

Output lands in `pipeline_playbook_generator/generated/`:
```
generated/
  <room_name>_action_playbook.md
  <room_name>_action_playbook_chunks.json
  pdfs/
    <room_name>_<domain>_action_playbook.pdf
```

## Configuration

All domain content lives in `config/playbook_blueprint.yml`. The generator reads the
kit metadata automatically — you only need to configure the content sections.

### Adding a domain

1. Add an entry under `domains:` in `config/playbook_blueprint.yml`
2. Set the key to partially match your `metadata/columns/*.yml` filename
3. Fill in `display_name`, `kpis_covered`, `scenarios`, `action_cards`, `example_plans`
4. Add a matching entry in `pipeline/pipeline_config.yml`:
   - Under `playbooks.sources`: add the PDF filename and `question_category`
   - Under `questions.seeds`: add the Deep Research question
   - Under `system_prompts`: add the LLM expert prompt

### Domain key matching

The domain key (for example, `sales_performance`) is matched against
`metadata/columns/*.yml` filenames using a partial string match. The key
`sales_performance` will match:
```
metadata/columns/sales_performance_metric_view.yml
```
because `sales_performance` appears in the filename stem.

## CLI reference

```
python pipeline_playbook_generator/generate_playbook.py [OPTIONS]

Options:
  --kit-format {genie_kit,legacy_contract}   Kit format (default: genie_kit)
  --kit-root PATH                   Repo root (default: parent of script dir)
  --output-dir PATH                 Where to write generated files (default: generated/)
  --pdf-output-dir PATH             Where to write PDFs, relative to output-dir (default: pdfs)
  --config PATH                     Blueprint config file (default: config/playbook_blueprint.yml)
```

## Requirements

The generator uses vendored dependencies in `.vendor/` so it can run offline in
Databricks. For local use, install:
```
pip install reportlab pyyaml
```

Or install from the requirements file if present:
```
pip install -r pipeline_playbook_generator/requirements.txt
```

## File structure

```
pipeline_playbook_generator/
  generate_playbook.py          Main script
  config/
    playbook_blueprint.yml      Domain content — EDIT THIS
  generated/                    Output (git-ignored by default)
    *.md                        Markdown playbook
    *.json                      Chunked JSON for debugging
    pdfs/                       PDFs ready to upload or index
  .vendor/                      Bundled Python deps (reportlab, etc.)
```

## Notes

- The `generated/` directory is safe to commit if you want to version the PDFs
- Re-running the generator is idempotent — it overwrites existing output
- If `snapshots/exported_space.json` is absent, the generator continues without it
- All paths in `pipeline_config.yml` must be filled in before running setup notebooks
