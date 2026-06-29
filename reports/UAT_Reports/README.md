# UAT Reports — Operations Review Package

This package contains checklists for the operations team to validate and sign off on a Genie room.

## How to Use

1. **Read** `00_overview_and_objectives.md` — Understand the review process and sign-off criteria
2. **Complete** `01_data_validation_checklist.md` — Validate KPI accuracy against source systems
3. **Complete** `02_genie_qa_checklist.md` — Test the room Q&A capability with all trained questions
4. **Complete** `03_insights_action_plans_checklist.md` — Review AI-generated insights quality
5. **Generate** the review guide: `python reports/UAT_Reports/scripts/generate_uat_report.py`

## Sign-Off Status

| Reviewer | Role | Status | Date |
|----------|------|--------|------|
| {{REVIEWER_1}} | Data Validation | {{STATUS_1}} | {{DATE_1}} |
| {{REVIEWER_2}} | Q&A Testing | {{STATUS_2}} | {{DATE_2}} |
| {{REVIEWER_3}} | Insights Review | {{STATUS_3}} | {{DATE_3}} |

## Directory Structure

```
UAT_Reports/
├── README.md
├── summaries/
│   ├── 00_overview_and_objectives.md
│   ├── 01_data_validation_checklist.md
│   ├── 02_genie_qa_checklist.md
│   └── 03_insights_action_plans_checklist.md
└── scripts/
    └── generate_uat_report.py
```
