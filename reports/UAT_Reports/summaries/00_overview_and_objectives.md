# UAT Review Overview — {{ROOM_TITLE}}

> **Review date:** {{REVIEW_DATE}} | **Room:** `{{ROOM_NAME}}`

## Purpose

This User Acceptance Testing (UAT) review validates that the Genie AI data room:
1. Returns accurate data aligned with source systems
2. Correctly answers all trained question templates
3. Produces useful insights and action plans

## Platform Components

| Component | Description |
|-----------|------------|
| Genie Room | AI data room with natural-language Q&A over metric views |
| Metric Views | Pre-computed KPI tables in Unity Catalog |
| Benchmarks | {{BENCHMARK_COUNT}} ground-truth question→SQL pairs for validation |
| Question Templates | {{EXAMPLE_SQL_COUNT}} trained question patterns |

## Review Structure

| Section | Content | Time Estimate | Owner |
|---------|---------|---------------|-------|
| Part 1: Data Validation | Verify KPI accuracy vs source | 2-3 hours | Data Analyst |
| Part 2: Genie Q&A | Test all {{EXAMPLE_SQL_COUNT}} question templates | 3-4 hours | OPS Lead |
| Part 3: Insights Review | Evaluate AI-generated insights | 1-2 hours | Manager |

## Sign-Off Criteria

| Item | Threshold | Result |
|------|-----------|--------|
| KPI accuracy vs source | > 95% match | PASS / FAIL |
| Q&A template pass rate | > 90% correct SQL | PASS / FAIL |
| Critical benchmark pass rate | 100% | PASS / FAIL |
| Insight relevance | > 80% actionable | PASS / FAIL |
