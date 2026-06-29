# Skill: promote_to_instruction

## Trigger
- "promote this snippet"
- "activate this example"
- "add this to the active set"
- "promote to instruction library"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `snippet_id` | User or identified from context | Yes |
| `snippet_type` | User | Yes (filters/measures/example_sql) |
| `check_capacity` | Auto | Yes |

## Steps

1. **Identify the snippet** — Find the file in `instruction_library/corpus/<type>/` by ID or name.

2. **Read the snippet** — Verify it has all required fields for its type.

3. **Check capacity** — Read `instruction_library/activation/limits.yml`:
   - Count currently active items of this type
   - Determine remaining budget
   - If AT CAPACITY: ask user which item to deactivate

4. **Add ID to activation manifest** — Append to `instruction_library/activation/<type>.active.yml`.

5. **Run materialize** — `python scripts/materialize.py`.

6. **Run validation** — `python scripts/validate.py`.

7. **Confirm promotion** — Report the snippet is now active.

## Deactivating to Make Room

If at capacity:
1. Show user a list of currently active items with their IDs and file names
2. Ask which to deactivate
3. Remove the deactivated ID from `instruction_library/activation/<type>.active.yml`
4. Add the deactivated ID to `instruction_library/isolated/deactivated.yml`
5. Then add the new ID and run materialize

## Outputs

- Updated `instruction_library/activation/<type>.active.yml`
- Updated `instructions/sql_snippets/<type>/` (after materialize)

## Validation

- [ ] Snippet exists in `instruction_library/corpus/<type>/`
- [ ] Snippet ID is now in the activation manifest
- [ ] Capacity limit not exceeded
- [ ] `python scripts/materialize.py` succeeds
- [ ] `python scripts/validate.py` returns 0 errors

## References

- `instruction_library/activation/limits.yml` — Capacity limits
- `docs/cap_management/` — Capacity management documentation
- `AGENTS.md` — Instruction library pipeline description
