# Skill: sync_room

## Trigger
- "push to room"
- "deploy to genie"
- "pull from room"
- "sync the room"
- "deploy the room"
- "update the live room"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `direction` | User | Yes (push or pull) |
| `env` | User | No (default: local) |

## Push Workflow (local → room)

1. **Read env/<env>.yml** — Confirm workspace_url, warehouse_id, space_id are set.

2. **Run validate** — `python scripts/validate.py` — Must return 0 errors.

3. **Run materialize** — `python scripts/materialize.py` — Materialize instruction_library → instructions/.

4. **Check capacity** — Confirm active counts are within limits.

5. **Run prepare** — `python scripts/prepare_eval.py --check-only` — Confirm READY status.

6. **Push** — `python scripts/push_folder_to_room.py --env <env>`.

7. **Verify push** — Check the output for success confirmation.

8. **Report** — Which components were updated (general, example_sql, filters, measures, benchmarks, sample_questions).

## Pull Workflow (room → local)

1. **Read env/<env>.yml** — Confirm space_id is set.

2. **Pull** — `python scripts/pull_room_to_folder.py --env <env>`.

3. **Review changes** — Check what was pulled vs. local files.

4. **Update instruction_library** — If the pull brought in new snippets, add them to `instruction_library/corpus/<type>/` as new files.

5. **Update activation manifests** — Ensure pulled IDs are reflected in `*.active.yml` manifests.

6. **Run validate** — `python scripts/validate.py`.

7. **Report** — What changed.

## Push Safety Checks

```
Before EVERY push:
1. python scripts/validate.py         → MUST return 0 errors
2. python scripts/materialize.py      → Must succeed
3. Capacity check                     → Must be within limits
4. python scripts/prepare_eval.py     → Must report READY
```

## Outputs

- (Push) Updated live Genie room
- (Pull) Updated local folder files

## Validation

- [ ] Validate returns 0 errors before pushing
- [ ] Push script reports success (HTTP 200)
- [ ] Post-push: verify room reflects changes in Databricks UI

## References

- `scripts/push_folder_to_room.py` — Push script
- `scripts/pull_room_to_folder.py` — Pull script
- `scripts/validate.py` — Validation script
- `scripts/materialize.py` — Materialization script
- `env/local.yml`, `env/prod.yml` — Environment configs
- `AGENTS.md` — Genie API reference
