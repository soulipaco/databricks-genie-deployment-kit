# Domain Capabilities — {{ROOM_TITLE}}

> **Report date:** {{REPORT_DATE}} | {{EXAMPLE_SQL_COUNT}} trained question templates

## Data Sources

### {{TABLE_1_NAME}} (`{{TABLE_1_IDENTIFIER}}`)

**Grain:** {{TABLE_1_GRAIN}}
**Date column:** `{{TABLE_1_DATE_COL}}` | **LOB column:** `{{TABLE_1_LOB_COL}}`

**Semantic Measures (use with MEASURE()):**
{{TABLE_1_MEASURES}}

**Key Dimensions:**
{{TABLE_1_DIMENSIONS}}

**Use Cases:**
{{TABLE_1_USE_CASES}}

---

## Question Templates

*Run `python reports/scripts/generate_inventory.py` to auto-populate all {{EXAMPLE_SQL_COUNT}} templates.*

{{QUESTION_TEMPLATES_LIST}}
