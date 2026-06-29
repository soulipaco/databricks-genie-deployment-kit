# Snapshots — Read-Only Bootstrap Artifacts

This directory stores read-only snapshots of the Genie room state.

## Files

| File | Purpose |
|------|---------|
| `exported_space.json` | Bootstrap snapshot pulled from the live room |
| `snapshot_YYYYMMDD_HHMMSS*.json` | Point-in-time snapshots from `python scripts/freeze.py` |

## Rules

- **NEVER edit snapshot files** — they are read-only reference artifacts
- The `exported_space.json` is used for bootstrap reference only
- New snapshots are created by `python scripts/freeze.py`
- Snapshots are NOT deployed back to the room
