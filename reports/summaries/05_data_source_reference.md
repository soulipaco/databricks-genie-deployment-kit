# Data Source Reference — {{ROOM_TITLE}}

> **Report date:** {{REPORT_DATE}} | {{TABLE_COUNT}} metric view(s)

## Table Reference

### `{{TABLE_1_IDENTIFIER}}`

**Description:** {{TABLE_1_DESCRIPTION}}
**Grain:** {{TABLE_1_GRAIN}}
**Date column:** `{{TABLE_1_DATE_COL}}`
**LOB column:** `{{TABLE_1_LOB_COL}}`

#### Semantic Measures

| Measure Column | Display Name | How to Use |
|----------------|-------------|------------|
| `{{MEASURE_1}}` | {{MEASURE_1_DISPLAY}} | `MEASURE({{MEASURE_1}})` |

#### Key Dimensions

| Column | Description |
|--------|------------|
| `{{DIM_COL_1}}` | {{DIM_COL_1_DESC}} |

---

*Run `python reports/scripts/generate_inventory.py` to auto-populate from kit metadata.*
