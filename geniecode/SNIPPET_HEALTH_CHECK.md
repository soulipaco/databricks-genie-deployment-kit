# Snippet Health Check — {{ROOM_NAME}}
> Procedures for auditing SQL snippets for quality, duplication, and convention compliance.

---

## Running the Health Check

```bash
# Full scan of all snippets
python geniecode/scripts/snippet_health_check.py --mode full

# Full scan with fix plan
python geniecode/scripts/snippet_health_check.py --mode full --fix-plan

# Scan one type only
python geniecode/scripts/snippet_health_check.py --mode full --type filters

# Single snippet by alias
python geniecode/scripts/snippet_health_check.py --mode single --target my_measure_alias

# JSON output
python geniecode/scripts/snippet_health_check.py --mode full --output json
```

---

## Check Categories

### CHK-1: Exact SQL Duplicates (HIGH)
Two or more snippets with identical normalized SQL.
- **Action if instructions differ:** MERGE instructions then DELETE copies
- **Action if instructions identical:** DELETE copies

### CHK-2: Alias Conflicts (CRITICAL)
Same alias, different SQL. Two snippets cannot have the same alias but different formulas.
- **Action:** Determine correct SQL variant; retire or re-alias others

### CHK-3: Display Name Conflicts (HIGH)
Same display_name, different SQL.
- **Action:** Differentiate display names or unify SQL

### CHK-4: Non-Qualified Table References (MEDIUM)
SQL references a table without the full `catalog.schema.` prefix.
- **Action:** Prefix with full `catalog.schema.` qualification

### CHK-5: Wrong Date Anchor in Dimensions (HIGH)
A date-output dimension references a table column instead of CURRENT_DATE().
- **Action:** Replace table column with CURRENT_DATE() expression

### CHK-6: MEASURE() vs Raw Conflict (HIGH)
Same alias has both a MEASURE() version and a raw calculation version.
- **Action:** Keep MEASURE() version; retire raw unless non-aggregation context

### CHK-7: Convention Violations (LOW/MEDIUM)
- 7a: Filter using BETWEEN instead of half-open pattern
- 7c: Dead-code CASE logic (WHEN 1=1, etc.)
- 7d: Missing instruction fields (WHEN_TO_USE, SCOPE_TABLES, RISK_IF_MISUSED)

---

## Severity Levels

| Severity | Action |
|----------|--------|
| CRITICAL | Fix before next deployment |
| HIGH | Fix in current sprint |
| MEDIUM | Fix when touching related files |
| LOW | Track but do not block deployment |

---

## Deduplication Decision Tree

```
Two snippets with identical SQL found (CHK-1):
├── Are their instructions (instruction/usage_guidance) identical?
│   ├── YES → Safe to DELETE one. Keep the one with better documentation.
│   └── NO → MERGE instructions into the canonical copy, then DELETE the duplicate.
│
├── Do they have the same alias (CHK-2)?
│   └── CRITICAL: Determine which SQL is correct. Re-alias or retire the wrong one.
│
└── Do they have the same display_name (CHK-3)?
    └── HIGH: Differentiate display names or confirm SQL is identical and merge.
```

---

## Capacity Impact

After deduplication, reclaim freed slots:
1. Update `instruction_library/activation/*.active.yml` to remove deleted IDs
2. Add deleted IDs to `instruction_library/isolated/*.isolated.yml` for record keeping
3. Run `python scripts/materialize.py` to update `instructions/`
4. Run `python scripts/validate.py` to confirm 0 errors
