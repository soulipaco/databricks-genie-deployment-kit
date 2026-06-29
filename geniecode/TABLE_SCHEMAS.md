# Table Schemas — {{ROOM_NAME}}
> **Last updated:** {{UPDATE_DATE}}
> Consolidated schema reference for all data tables.
> Replace all {{PLACEHOLDER}} values with actual table schemas for this room.

---

## 1. {{TABLE_1_DISPLAY_NAME}} (`{{CATALOG}}.{{SCHEMA}}.{{TABLE_1}}`)
**Grain:** {{TABLE_1_GRAIN_DESCRIPTION}}
**Date column:** `{{TABLE_1_DATE_COL}}` | **LOB column:** `{{TABLE_1_LOB_COL}}`

### Semantic Measures (use with MEASURE())
`{{MEASURE_1}}`, `{{MEASURE_2}}`, `{{MEASURE_3}}`, `{{MEASURE_4}}`, `{{MEASURE_5}}`

### Key Dimensions (with entity matching enabled)
`{{DIM_1}}`, `{{DIM_2}}`, `{{DIM_3}}`, `{{DIM_4}}`, `{{DIM_5}}`

### Other Dimensions
`{{OTHER_DIM_1}}`, `{{OTHER_DIM_2}}`, `{{OTHER_DIM_3}}`

### Notes
- {{TABLE_1_NOTE_1}}
- {{TABLE_1_NOTE_2}}

---

## 2. {{TABLE_2_DISPLAY_NAME}} (`{{CATALOG}}.{{SCHEMA}}.{{TABLE_2}}`)
**Grain:** {{TABLE_2_GRAIN_DESCRIPTION}}
**Date column:** `{{TABLE_2_DATE_COL}}` | **LOB column:** `{{TABLE_2_LOB_COL}}`

### Semantic Measures (use with MEASURE())
`{{MEASURE_A}}`, `{{MEASURE_B}}`, `{{MEASURE_C}}`

### Key Dimensions
`{{DIM_A}}`, `{{DIM_B}}`, `{{DIM_C}}`

### Notes
- {{TABLE_2_NOTE_1}}

---

## Scope Restrictions Summary

| Measure / Column | Allowed at | NOT allowed at |
|-----------------|------------|---------------|
| {{RESTRICTED_MEASURE_1}} | {{ALLOWED_GRAIN}} | {{FORBIDDEN_GRAIN}} |
| {{RESTRICTED_MEASURE_2}} | {{ALLOWED_GRAIN_2}} | {{FORBIDDEN_GRAIN_2}} |

---

## How to Add a New Table Schema

1. Add the table to `data_sources/tables.yml`
2. Create `metadata/columns/<table>.yml` with column configurations
3. Add a new section to this file following the template above
4. Update `geniecode/KNOWLEDGE_BASE.md` source routing table
5. Update `geniecode/SELECT_STRATEGY.md` domain routing
6. Update `geniecode/DOMAIN_RULES.md` with any domain-specific rules
7. Update `instructions/general.md` with grain logic and KPI rules
