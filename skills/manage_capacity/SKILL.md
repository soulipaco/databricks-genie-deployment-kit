# Skill: manage_capacity

## Trigger
- "check capacity"
- "how much room is left"
- "manage instruction capacity"
- "what is the capacity status"
- "we are at capacity"

## Inputs

None required — reads from activation manifests automatically.

## Steps

1. **Read instruction_library/activation/limits.yml** — Load the capacity budget configuration.

2. **Count table descriptions** — Count tables in `data_sources/tables.yml`.

3. **Calculate the example_sql budget**:
   ```
   total = 100
   general = 1
   tables = N
   example_sql_budget = total - general - tables
   ```

4. **Count active assets** — Read each activation manifest:
   - `instruction_library/activation/filters.active.yml` → count IDs
   - `instruction_library/activation/measures.active.yml` → count IDs
   - `instruction_library/activation/example_sql.active.yml` → count IDs

5. **Produce a capacity status report**:
   ```
   Capacity Status — <room_name>
   
   Total budget:          100
   General instruction:    -1
   Table descriptions:    -N
   Available (example_sql): XX
   Currently active (example_sql): XX
   Remaining (example_sql): XX
   
   Filters: XX active (cap: 100)
   Measures: XX active (cap: 100)
   
   Status: OK / WARNING (N over budget)
   ```

6. **If at or near capacity for example_sql:**
   a. Run `python geniecode/scripts/snippet_health_check.py --mode full --fix-plan`
   b. Identify any CHK-1 (exact duplicates) that can be merged
   c. Review `instruction_library/isolated/` for already-deactivated items
   d. Suggest candidates for deactivation based on:
      - Duplicate SQL (CHK-1)
      - Narrow use cases covered by a broader example
      - Low recent relevance

7. **To deactivate a snippet:**
   a. Remove its ID from the activation manifest
   b. Add it to `instruction_library/isolated/deactivated.yml`
   c. Run `python scripts/materialize.py`
   d. Run `python scripts/validate.py`

## Outputs

- Capacity status report
- List of deactivation candidates (if at/near limit)

## Validation

- [ ] Active example_sql count ≤ `example_sql_budget`
- [ ] Active filters count ≤ 100
- [ ] Active measures count ≤ 100
- [ ] After deactivation: capacity is within limits
- [ ] `python scripts/validate.py` returns 0 errors

## References

- `instruction_library/activation/limits.yml` — Capacity budget config
- `geniecode/SNIPPET_HEALTH_CHECK.md` — Duplicate detection procedures
- `docs/cap_management/` — Capacity management documentation
