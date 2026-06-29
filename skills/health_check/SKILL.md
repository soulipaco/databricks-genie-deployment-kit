# Skill: health_check

## Trigger
- "run health check"
- "validate the kit"
- "check the room configuration"
- "audit the deployment kit"
- "run snippet health check"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `check_scope` | User | No (default: full) |

## Steps

### Phase 1: Structure Validation
1. Run `python scripts/validate.py` — Report all errors and warnings.
2. Check required files exist:
   - `room.config.yml`
   - `data_sources/tables.yml`
   - `instructions/general.md`
   - `instruction_library/activation/limits.yml`
   - Each table in tables.yml has a matching `metadata/columns/*.yml`

### Phase 2: Snippet Health Check
3. Run `python geniecode/scripts/snippet_health_check.py --mode full --fix-plan`.
4. Report issues by category:
   - CHK-1: Exact SQL duplicates
   - CHK-2: Alias conflicts
   - CHK-3: Display name conflicts
   - CHK-4: Non-qualified table references
   - CHK-5: Wrong date anchor in dimensions
   - CHK-6: MEASURE() vs raw conflicts
   - CHK-7: Convention violations

### Phase 3: ID Uniqueness Check
5. Verify no ID appears more than once within each asset category:
   - All benchmark IDs unique
   - All example_sql IDs unique
   - All filter IDs unique
   - All measure IDs unique

### Phase 4: Capacity Check
6. Read `instruction_library/activation/limits.yml`.
7. Count active assets in each activation manifest.
8. Calculate remaining capacity:
   - Total: 100
   - Minus general: -1
   - Minus tables: -N (count from data_sources/tables.yml)
   - Available for example_sql: 100 - 1 - N
9. Report any types at or near capacity.

### Phase 5: Hardcoded Date Check
10. Search all YAML files for date strings matching `YYYY-MM-DD` pattern.
11. Report files with hardcoded dates (should have `_cleanup_flags` set).

### Phase 6: Convention Check
12. Spot-check 5 random filter SQL entries for `ILIKE` usage.
13. Spot-check 5 random example SQL entries for dynamic date usage.
14. Spot-check 5 random example SQL entries for 3-level table qualification.

### Phase 7: Report
15. Produce a structured health report:
    ```
    Health Check Report — <room_name>
    Date: <date>
    
    Structure: PASS / FAIL (N errors)
    Snippet Health: PASS / FAIL (N issues)
    ID Uniqueness: PASS / FAIL
    Capacity: OK (N remaining) / WARNING (near limit)
    Hardcoded Dates: PASS / FAIL (N files)
    Conventions: PASS / WARN
    
    Action Items:
    - ...
    ```

## Outputs

- Health report (written to `build/health_check_<date>.txt` if requested)
- List of action items by priority

## Validation

- [ ] Structure check returns 0 errors
- [ ] All CHK-1 through CHK-7 issues triaged
- [ ] ID uniqueness confirmed
- [ ] Capacity within limits
- [ ] No unflagged hardcoded dates

## References

- `geniecode/SNIPPET_HEALTH_CHECK.md` — Detailed check procedures
- `geniecode/scripts/snippet_health_check.py` — Executable check script
- `scripts/validate.py` — Structure validation script
- `instruction_library/activation/limits.yml` — Capacity limits
- `docs/cap_management/` — Capacity management documentation
