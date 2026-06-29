# Skill: update_geniecode

## Trigger
- "update your knowledge base"
- "refresh your context"
- "rescan the repo"
- "sync your knowledge"
- "refresh geniecode"
- "update geniecode"

## Inputs

None required — reads from the kit directory automatically.

## Steps

See `geniecode/SELF_UPDATE.md` for the full 7-step protocol. Summary:

1. **Scan for structural changes** — Count files in key directories and compare to KNOWLEDGE_BASE.md baseline.

2. **Re-read configuration files:**
   - `room.config.yml`
   - `data_sources/tables.yml`
   - `instructions/general.md`
   - `instructions/general_enriched.md` (if exists)

3. **Check column metadata** — Re-read `metadata/columns/<table>.yml` for each table.

4. **Check activation manifests:**
   - `instruction_library/activation/filters.active.yml`
   - `instruction_library/activation/measures.active.yml`
   - `instruction_library/activation/example_sql.active.yml`
   - `instruction_library/activation/limits.yml`

5. **Spot-check new assets** — If new files found, read 2-3 samples.

6. **Update all geniecode files:**
   - `geniecode/KNOWLEDGE_BASE.md` — Update asset counts, routing table, date logic
   - `geniecode/DOMAIN_RULES.md` — Update any changed domain rules
   - `geniecode/TABLE_SCHEMAS.md` — Update schema for changed tables
   - `geniecode/FILE_FORMATS.md` — Update if new file types added
   - `geniecode/SELF_UPDATE.md` — Update scan list if kit structure changed
   - `geniecode/SELECT_STRATEGY.md` — Update routing if tables changed
   - `geniecode/BENCHMARK_WORKSPACE.md` — Update if taxonomy changed
   - `geniecode/FIX_PATTERNS.md` — Add any new patterns discovered

7. **Report to user:**
   - What changed (counts, rules, structure)
   - Any issues found
   - Confirmation that knowledge base is current

## Outputs

- Updated `geniecode/KNOWLEDGE_BASE.md`
- Updated other geniecode files as needed
- Summary report to user

## Validation

- [ ] KNOWLEDGE_BASE.md asset counts match actual file counts
- [ ] Source routing table reflects current `data_sources/tables.yml`
- [ ] Activation manifest IDs reflected in KNOWLEDGE_BASE.md
- [ ] All updated files pass YAML syntax validation

## References

- `geniecode/SELF_UPDATE.md` — Full 7-step protocol
- `geniecode/KNOWLEDGE_BASE.md` — Fast context loader (to update)
- `geniecode/TABLE_SCHEMAS.md` — Schema reference (to update)
- `geniecode/DOMAIN_RULES.md` — Domain rules (to update)
