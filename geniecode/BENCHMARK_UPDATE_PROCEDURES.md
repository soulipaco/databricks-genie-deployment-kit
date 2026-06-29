# Benchmark Update Procedures — {{ROOM_NAME}}
> **Last updated:** {{UPDATE_DATE}}
> Step-by-step playbook for AI coding agents when processing benchmark evaluation results.

---

## When This Procedure Triggers

User shares benchmark evaluation results containing:
- **Question:** The natural language question
- **Assessment:** Pass / Bad
- **Score reason:** Missing Columns / Wrong Metric / Wrong Values / Other
- **Model SQL + output data:** What the Genie room generated
- **Ground Truth (GT) SQL + output data:** Expected correct answer

---

## Master Decision Flowchart (10 Steps)

```
STEP 1: TRIAGE
  Is the assessment "Bad"?
  +-- NO --> PASS, no action needed
  +-- YES --> Go to STEP 2

STEP 2: FIND & READ MATCHING SNIPPET (MANDATORY — do before any analysis)
  a) Search instructions/example_sql/ for the active snippet whose question
     pattern most closely matches the benchmark question.
  b) ACTUALLY READ the snippet file — do NOT skip this or guess from filename.
  c) Read its SQL, parameters, and full usage_guidance.
  d) If no active snippet matches, search instruction_library/corpus/example_sql/
     for an inactive candidate.
  e) Record: snippet ID, filename, active or library-only.

STEP 3: THREE-WAY COMPARISON (Critical Step)
  Compare THREE things side-by-side:
    a) The benchmark GT SQL
    b) The model output SQL
    c) The actual snippet SQL + usage_guidance from STEP 2
  For each dimension, note differences:
    - Date range / date column
    - Column list (output shape)
    - ORDER BY / LIMIT
    - Measures / aggregations used
    - Table / source routing
    - Aggregation logic

STEP 4: SNIPPET CONSISTENCY CHECK
  Scan the snippet usage_guidance for:
    a) INTERNAL contradictions (two lines giving opposite instructions)
    b) CROSS-SNIPPET conflicts (another active snippet covers same pattern differently)
    c) GUIDANCE vs SQL mismatch (snippet SQL disagrees with its own guidance)
  If ANY contradiction is found, flag as contributing root cause.

STEP 5: CLASSIFY ROOT CAUSE
  Assign exactly ONE primary class:
    1. OUTPUT-SHAPE         -- Model logic correct, output format differs from GT
    2. SEMANTIC-GENERATION  -- Model generated wrong logic/table/measure
    3. BENCHMARK-DEFECT     -- GT itself is wrong, over-scoped, or outdated
    4. EVALUATOR-FRAGILITY  -- Evaluator flagged a false negative
    5. MIXED                -- Both GT and model have issues (fix both)
    6. RETRIEVAL-COLLISION  -- Model retrieved a similar but wrong example_sql
    7. SNIPPET-CONTRADICTION -- Snippet guidance contradicts itself or its SQL

STEP 6: DETERMINE FIX TARGET(S)
  Map the class to what needs changing (see Fix Target Matrix below).

STEP 7: CHECK FOR BATCH APPLICABILITY
  Does the same root cause affect multiple benchmarks?
  If yes, identify ALL affected benchmarks and fix them together.

STEP 8: APPLY FIX(ES)
  Follow the specific procedure for each fix target type.

STEP 9: VALIDATE
  Run: python scripts/validate.py
  Verify 0 errors, 0 warnings.

STEP 10: LOG
  Update docs/11_failed_evaluation_tracking.md with:
  - Benchmark ID, question, class, evidence, fix applied
  Update geniecode/FIX_PATTERNS.md if this is a new pattern.
```

---

## Fix Target Matrix

| Root-Cause Class | Benchmark | Example SQL | Filter/Measure | General.md |
|-----------------|-----------|-------------|----------------|------------|
| OUTPUT-SHAPE | UPDATE GT | - | - | - |
| SEMANTIC-GENERATION | - | ADD/UPDATE | maybe | maybe |
| BENCHMARK-DEFECT | UPDATE GT | - | - | - |
| EVALUATOR-FRAGILITY | optional | - | - | - |
| MIXED | UPDATE GT | ADD/UPDATE | maybe | maybe |
| RETRIEVAL-COLLISION | - | TIGHTEN guidance | - | maybe |
| SNIPPET-CONTRADICTION | - | FIX guidance | - | - |

---

## Fix Procedures by Target Type

### Procedure A: Update a Benchmark GT

**When:** GT is wrong, over-scoped, or uses outdated conventions.

**Steps:**
1. Locate the file: `benchmarks/<NN>_<slug>.yml`
2. Read current file — **PRESERVE the `id` field!**
3. Verify the question text matches the intended question
4. Write corrected SQL following these rules:
   - Dynamic dates only (CURRENT_DATE expressions), never hardcoded
   - 3-level fully qualified table names: `catalog.schema.table`
   - Only columns relevant to the question
   - Follow room output shape conventions (percentages, volumes, ordering)
   - Half-open date windows
5. If fixing hardcoded dates, remove from `_cleanup_flags`
6. Validate YAML syntax

### Procedure B: Update/Create an Example SQL

**When:** Model generated wrong logic due to missing or incorrect example.

**Steps:**
1. **3-way search:** Check `instructions/example_sql/` AND `instruction_library/corpus/example_sql/`
2. If related example EXISTS but is wrong:
   - Fix the SQL, `usage_guidance`, or ordering
   - Update BOTH library AND active copies
3. If correct example exists in LIBRARY but is NOT ACTIVE:
   - Evaluate if it should be activated
   - Check capacity: `instruction_library/activation/limits.yml`
   - If AT CAPACITY: must deactivate one to add
4. If NO related example exists:
   - Generate new ID: `python -c "import uuid; print(uuid.uuid4().hex)"`
   - Create in `instruction_library/corpus/example_sql/` first
   - Parameterize: `:StartDate`, `:EndDateExclusive`, `:PeriodGrain`
   - Add `usage_guidance` with explicit scope and anti-patterns
   - Activate only if within budget
5. **For retrieval collisions:** Tighten the WRONG example's `usage_guidance`:
   - Add "DO NOT use for..." exclusion text
   - Narrow the question patterns it should match

### Procedure C: Update Filter/Measure Snippets

**When:** A missing or wrong filter/measure pattern caused the failure.

**Steps:**
1. Search `instructions/sql_snippets/filters/` or `measures/`
2. Update or create following FILE_FORMATS.md specs
3. Include `instruction` with WHEN_TO_USE, SCOPE_TABLES, RISK_IF_MISUSED
4. Run `python scripts/materialize.py` after changes

### Procedure D: Update General Instructions

**When:** Systemic rule missing or ambiguous, affecting multiple benchmarks.

**Steps:**
1. Read `instructions/general.md`
2. Identify the correct section for the rule
3. Draft the rule — ensure no contradiction with existing rules
4. Also update `general_enriched.md` if it exists
5. **CAUTION:** general.md changes affect ALL queries. High impact.

### Procedure E: Fix Snippet Contradiction

**When:** A snippet guidance has internal contradictions.

**Steps:**
1. Identify the EXACT contradictory lines (quote them verbatim)
2. Determine which line is CORRECT by cross-referencing:
   a) The snippet SQL (source of truth for that snippet)
   b) The benchmark GT SQL
   c) The general.md rules
   d) DOMAIN_RULES.md conventions
3. REMOVE or REWRITE the incorrect line. Do NOT leave both lines.
4. Update BOTH `instructions/example_sql/<file>` AND `instruction_library/corpus/example_sql/<file>`
5. Verify fix does not introduce new contradictions

---

## Quality Checks Before Committing

- [ ] SQL uses correct source table for the domain?
- [ ] SQL uses correct date column for this table?
- [ ] SQL uses correct grouping/identity columns?
- [ ] All dates are dynamic (no hardcoded)?
- [ ] Text filters use ILIKE?
- [ ] Filtered dimensions in SELECT?
- [ ] Only question-relevant columns in output?
- [ ] YAML format correct? `id` field preserved?
- [ ] Consistent with DOMAIN_RULES.md?
- [ ] Matching snippet read and checked for contradictions?
- [ ] Snippet usage_guidance consistent with its own SQL?
- [ ] No cross-snippet conflicts for same question pattern?
- [ ] Validation passes: python scripts/validate.py
