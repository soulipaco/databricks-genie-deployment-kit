# 06 — Question Taxonomy

Classify all benchmark questions using this taxonomy before generating.

## Category A: Summary / Ranking by Dimension
- Questions: "What is [KPI] by [dimension]?", "How does [KPI] vary by [dimension]?"
- SQL pattern: `SELECT dim, MEASURE(kpi) ... GROUP BY ALL ORDER BY metric DESC`
- Date scope: parameterized or last month default

## Category B: Trend Analysis
- Questions: "How has [KPI] trended over [period]?", "Show weekly [KPI] trend"
- SQL pattern: `SELECT DATE_TRUNC(period, date_col) AS period, MEASURE(kpi) ... GROUP BY ALL ORDER BY period`
- Date scope: last 12 weeks or last 6 months

## Category C: Top-N / Bottom-N Ranking
- Questions: "Who are the top 5 [entities] by [KPI]?", "Worst N [entities]"
- SQL pattern: Category A + `LIMIT N` (default N=5)
- Ordering: DESC for "top" / "best"; ASC for "bottom" / "worst"

## Category D: Comparison
- Questions: "How does [X] compare to [Y]?", "Compare last month vs previous month"
- SQL pattern: CTEs or conditional aggregation
- Sub-types: period-over-period, entity-vs-average, two entities

## Category E: Pareto / Root-Cause
- Questions: "What are the top reasons for [X]?", "Pareto of [issue category]"
- SQL pattern: SUM + cumulative percentage
- May require raw table (not metric view) for row-level analysis

## Category F: Individual Entity Lookup
- Questions: "Show me [person]'s [KPI]", "What is [entity]'s performance?"
- SQL pattern: Single filter + SELECT all relevant KPIs
- Requires ILIKE for entity matching

## Category G: Parameterized Date Range
- Questions with explicit dates: "For Q1...", "Between Jan and Mar..."
- SQL pattern: Uses `:StartDate`, `:EndDateExclusive` parameters

## Category H: Complex Multi-Step
- Questions requiring CTEs, window functions, or multi-pass logic
- Example: "Leave-one-out agent impact", "Change from threshold", "Percentile distribution"
