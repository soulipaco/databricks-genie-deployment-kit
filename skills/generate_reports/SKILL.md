# Skill: generate_reports

## Trigger
- "generate the report"
- "generate reports"
- "create the capability report"
- "generate the uat guide"
- "build the stakeholder report"
- "export the room as a PDF"
- "generate inventory"

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `report_type` | User | No (default: full — all reports) |
| `engine` | User | No (default: html-only) |

Supported `report_type` values: `full`, `inventory-only`, `summaries-only`, `uat-only`
Supported `engine` values: `html-only`, `weasyprint`, `pdfkit`

## Steps

### Phase 1: Generate Inventory Data

1. **Run generate_inventory.py** to scan the kit and produce all 7 JSON data files:
   ```bash
   python reports/scripts/generate_inventory.py
   ```

2. **Review the output** — confirm all 7 files are written to `reports/data/`:
   - `room_identity.json`
   - `domain_capabilities.json`
   - `benchmark_inventory.json`
   - `snippet_inventory.json`
   - `evaluation_history.json`
   - `sales_ready_questions.json`
   - `data_sources.json`

3. **Review auto-generated summaries** — `generate_inventory.py` also writes starter markdown summaries to `reports/summaries/`. Check if they need narrative content added.

### Phase 2: Enhance Markdown Summaries (Optional)

4. **Read each generated summary** in `reports/summaries/` and enhance with:
   - Narrative context about the room's purpose and business value
   - Per-domain capability descriptions
   - Engineering notes on evaluation history
   - Next steps and roadmap items

5. For the **sales-ready overview** (`00_sales_ready_overview.md`):
   - Add a capability matrix with per-domain question counts
   - List representative questions from each domain
   - Add business value messaging

### Phase 3: Generate HTML/PDF Reports

6. **Generate main capability report**:
   ```bash
   # HTML only (no dependencies)
   python reports/scripts/generate_report.py

   # PDF (requires weasyprint)
   pip install markdown weasyprint
   python reports/scripts/generate_report.py --engine weasyprint
   ```

7. **Generate UAT review guide**:
   ```bash
   python reports/UAT_Reports/scripts/generate_uat_report.py
   ```

8. **Verify outputs** — confirm these files exist:
   - `reports/<room_name>_Report.html`
   - `reports/<room_name>_Report.pdf` (if PDF engine used)
   - `reports/UAT_Reports/<room_name>_UAT_Guide.html`

### Phase 4: Customize UAT Checklists

9. **Populate data validation checklist** (`reports/UAT_Reports/summaries/01_data_validation_checklist.md`):
   - Replace `{{KPI_*}}` placeholders with actual KPI names from the room
   - Replace `{{DOMAIN_*}}` placeholders with actual domain names
   - Set the review period and reviewer name

10. **Populate Q&A checklist** (`reports/UAT_Reports/summaries/02_genie_qa_checklist.md`):
    - Pull question list from `reports/data/domain_capabilities.json`
    - Group by category (A through H per `docs/06_question_taxonomy.md`)
    - Replace sample question placeholders with actual questions

## Outputs

- `reports/data/*.json` — 7 JSON inventory files (machine-readable)
- `reports/summaries/*.md` — 7 markdown summaries (human-readable)
- `reports/<room_name>_Report.html` — Main capability report (HTML)
- `reports/<room_name>_Report.pdf` — Main capability report (PDF, optional)
- `reports/UAT_Reports/<room_name>_UAT_Guide.html` — UAT review guide (HTML)
- `reports/UAT_Reports/<room_name>_UAT_Guide.pdf` — UAT review guide (PDF, optional)

## What Each Report Is For

| Report | Audience | When to Generate |
|--------|----------|--------------------|
| `00_sales_ready_overview.md` | Sales / demo | Before any stakeholder demo |
| `01_executive_summary.md` | Management | After each major deployment |
| `02_domain_capabilities.md` | Technical buyers | During pre-sales or onboarding |
| `03_benchmark_coverage.md` | QA / validation | Before UAT sign-off |
| `04_evaluation_progress.md` | Engineering | After each evaluation cycle |
| `05_data_source_reference.md` | Technical | At initial deployment |
| `06_fix_history_and_patterns.md` | Engineering | Monthly or per evaluation sprint |
| UAT Guide | OPS team | Before formal sign-off |

## Validation

- [ ] `reports/data/` contains all 7 JSON files
- [ ] `reports/summaries/` contains all 7 markdown files
- [ ] `reports/<room_name>_Report.html` exists and opens correctly in a browser
- [ ] UAT guide HTML exists
- [ ] No `{{PLACEHOLDER}}` values remain in the final HTML output (filled by inventory script)

## References

- `reports/scripts/generate_inventory.py` — Inventory generation script
- `reports/scripts/generate_report.py` — Report generation script
- `reports/UAT_Reports/scripts/generate_uat_report.py` — UAT report script
- `reports/README.md` — Full reporting system overview
- `geniecode/KNOWLEDGE_BASE.md` — Room identity and asset counts
