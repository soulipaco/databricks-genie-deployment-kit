# 13 — Usage Guidance Migration Policy

## Goal

Ensure every active example_sql has a properly structured `usage_guidance` field
that prevents retrieval collisions and guides model behavior.

## Migration Strategy

### Step 1: Audit
For each file in `instruction_library/corpus/example_sql/`:
- Does it have `usage_guidance`?
- Does `usage_guidance` have TRIGGER PHRASES?
- Does `usage_guidance` have anti-patterns if needed?

### Step 2: Prioritize
Migrate active snippets first. Inactive corpus items can wait.

### Step 3: Add TRIGGER PHRASES
Identify all question variants this example should cover.
List them explicitly. This prevents retrieval collision.

### Step 4: Add Anti-Patterns
For each example that competed with another similar example in evaluations,
add explicit "Do NOT use for..." exclusions.

### Step 5: Validate
`python scripts/validate.py` — 0 errors required.
