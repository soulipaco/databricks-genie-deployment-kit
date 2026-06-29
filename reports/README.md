# Reports

This directory contains the reporting and stakeholder communication layer for the Genie Room Deployment Kit.

## What This System Provides

- **Auto-inventory** — Scans the kit and generates structured JSON data files cataloging all room capabilities
- **Markdown summaries** — 7 human-readable reports covering sales capability, management overview, benchmark coverage, evaluation progress, and engineering history
- **PDF/HTML generation** — Produces printable reports from the markdown summaries
- **UAT review package** — Data validation and Q&A checklists for operations sign-off

## Workflow

```
Step 1: Generate inventory data (reads the kit, outputs JSON)
  python reports/scripts/generate_inventory.py

Step 2: Review/edit markdown summaries (auto-generated stubs)
  → Edit reports/summaries/*.md to add narrative and context

Step 3: Generate HTML/PDF reports
  python reports/scripts/generate_report.py --engine html-only
  # For PDF: pip install markdown weasyprint
  # python reports/scripts/generate_report.py --engine weasyprint
```

## Directory Structure

```
reports/
├── README.md                          # This file
├── <ROOM_NAME>_Report.html            # Generated report (HTML)
├── <ROOM_NAME>_Report.pdf             # Generated report (PDF, optional)
├── <ROOM_NAME>_UAT_Guide.html         # Generated UAT guide
├── data/                              # Auto-generated JSON inventory files
│   ├── room_identity.json             # Room metadata, capacity, environment
│   ├── domain_capabilities.json       # All example SQL with parameters
│   ├── benchmark_inventory.json       # All benchmark test cases
│   ├── snippet_inventory.json         # All filters, measures, dimensions
│   ├── evaluation_history.json        # Evaluation tracking (if available)
│   ├── sales_ready_questions.json     # Question catalog with business mapping
│   └── data_sources.json             # Full schema reference
├── summaries/                         # Markdown reports (human-authored/auto-generated)
│   ├── 00_sales_ready_overview.md     # Capability matrix + question catalog (sales)
│   ├── 01_executive_summary.md        # Management overview and room health
│   ├── 02_domain_capabilities.md      # Technical per-domain deep-dive
│   ├── 03_benchmark_coverage.md       # Ground-truth test coverage
│   ├── 04_evaluation_progress.md      # Evaluation timeline and failure analysis
│   ├── 05_data_source_reference.md    # Schema and SQL reference
│   └── 06_fix_history_and_patterns.md # Engineering work log
├── scripts/
│   ├── generate_inventory.py          # Scans kit → generates data/*.json
│   └── generate_report.py             # Reads summaries/*.md → HTML/PDF
└── UAT_Reports/
    ├── README.md
    ├── summaries/
    │   ├── 00_overview_and_objectives.md
    │   ├── 01_data_validation_checklist.md
    │   ├── 02_genie_qa_checklist.md
    │   └── 03_insights_action_plans_checklist.md
    └── scripts/
        └── generate_uat_report.py
```

## Output Files

| File | Audience | Content |
|------|----------|---------|
| `summaries/00_sales_ready_overview.md` | Sales / demos | Full question catalog, capability matrix |
| `summaries/01_executive_summary.md` | Management | Room health, status, coverage |
| `summaries/02_domain_capabilities.md` | Technical buyers | Per-table schema + all question templates |
| `summaries/03_benchmark_coverage.md` | QA / validation | All 168+ test cases |
| `summaries/04_evaluation_progress.md` | Engineering | Evaluation history + failure taxonomy |
| `summaries/05_data_source_reference.md` | Technical | Schema reference + sample SQL |
| `summaries/06_fix_history_and_patterns.md` | Engineering | Fix work log + discovered patterns |
| `UAT_Reports/summaries/` | OPS team | Validation checklists for room sign-off |
