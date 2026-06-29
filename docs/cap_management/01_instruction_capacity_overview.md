# Instruction Capacity Overview

## Capacity Budget

The Genie API allows a maximum of **100 total space instructions** per room.

```
Total budget:                100
- General instruction:        -1 (always 1)
- Table descriptions:         -N (one per table in data_sources/tables.yml)
- Available for example_sql:  100 - 1 - N
```

Filters and measures have their own independent cap (100 each).

## Capacity Configuration

Capacity is configured in `instruction_library/activation/limits.yml`.

## Monitoring

To check current capacity:
```bash
python scripts/materialize.py --check-limits
```

Output shows:
- Total budget breakdown
- Active counts per type
- Remaining capacity
- Status: OK / WARNING

## What to Do When at Capacity

1. Run snippet health check: `python geniecode/scripts/snippet_health_check.py --mode full --fix-plan`
2. Identify CHK-1 exact duplicates that can be merged
3. Review inactive candidates in `instruction_library/isolated/deactivated.yml`
4. Deactivate lower-priority items (remove IDs from `*.active.yml`)
5. Run `python scripts/materialize.py` to update `instructions/`
