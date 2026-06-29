# {{ROOM_TITLE}} — Sales-Ready Capability Overview

> **Room:** `{{ROOM_NAME}}` | **Report date:** {{REPORT_DATE}} | **Source of truth:** repo

## At-a-Glance Capability Matrix

| Metric | Count |
|--------|-------|
| Example SQL Templates | {{EXAMPLE_SQL_COUNT}} |
| Benchmark Test Cases | {{BENCHMARK_COUNT}} |
| SQL Snippets | {{SNIPPET_COUNT}} ({{FILTER_COUNT}} filters, {{MEASURE_COUNT}} measures, {{DIM_COUNT}} dimensions) |
| Data Sources (Metric Views) | {{TABLE_COUNT}} |

## What This Room Answers

{{ROOM_CAPABILITY_SUMMARY}}

## Domain Coverage

| Domain | Templates | Benchmarks | Total Answerable |
|--------|-----------|------------|------------------|
| {{DOMAIN_1}} | {{DOMAIN_1_TEMPLATES}} | {{DOMAIN_1_BENCHMARKS}} | {{DOMAIN_1_TOTAL}} |
| {{DOMAIN_2}} | {{DOMAIN_2_TEMPLATES}} | {{DOMAIN_2_BENCHMARKS}} | {{DOMAIN_2_TOTAL}} |

## Sample Questions the Room Can Answer

{{LIST_OF_REPRESENTATIVE_QUESTIONS}}

## Health Metrics

| Health Indicator | Status |
|-----------------|--------|
| Example SQL Templates | {{EXAMPLE_SQL_COUNT}} / {{EXAMPLE_SQL_BUDGET}} capacity |
| Benchmark Coverage | {{BENCHMARK_COUNT}} ground-truth test cases |
| SQL Snippets | {{SNIPPET_COUNT}} |
| Evaluation Sessions | {{EVAL_SESSION_COUNT}} |
| Pass Rate | {{PASS_RATE}} |

---

*Run `python reports/scripts/generate_inventory.py` to auto-populate this report from the kit.*
