# Benchmarks

Ground-truth question → SQL pairs for evaluating Genie room accuracy.

## File Naming
`NN_slug.yml` — Sequential number + descriptive slug.

## Format

```yaml
id: <32-char hex>
question: <natural language question>
answer_format: SQL
sql: <ground-truth SQL>
_cleanup_flags: [...]   # Optional — hardcoded dates to fix
```

## Rules

- IDs must be globally unique within `benchmarks/`
- SQL must use 3-level table qualification
- No hardcoded dates (or flag in `_cleanup_flags`)
- Text filters must use ILIKE
- Ground truth should answer the stated question exactly and minimally

## See Also

- `skills/generate_benchmarks/SKILL.md` — How to generate benchmarks
- `geniecode/BENCHMARK_UPDATE_PROCEDURES.md` — How to fix failing benchmarks
- `docs/06_question_taxonomy.md` — Question classification taxonomy
