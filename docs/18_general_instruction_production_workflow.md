# 18 — General Instruction Production Workflow

## Purpose

`instructions/general.md` is the highest-impact single file in the room.
It governs all queries globally. Changes here affect every question.

## Content Structure

A well-structured `instructions/general.md` should include:

1. **Source Routing** — Which table to use for which type of question
2. **Grain Rules** — What each table's row represents
3. **Date Logic** — Calendar month, rolling days, default windows
4. **Aggregation Rules** — MEASURE() conventions, GROUP BY ALL
5. **Output Conventions** — Percentage formatting, ordering, default LIMIT
6. **Identity Rules** — Which columns to use for entities
7. **Special Cases** — Domain-specific exceptions and edge cases

## Authoring Procedure

1. **Read geniecode/DOMAIN_RULES.md** — Use as the authoritative source for each rule
2. **Draft the general.md section by section** using DOMAIN_RULES.md as input
3. **Check for contradictions** with existing snippets
4. **Test high-impact rules** with at least 5 benchmark questions
5. **Deploy and evaluate** — Run benchmark evaluation after changes
6. **Update DOMAIN_RULES.md** if new rules are discovered

## High-Impact Rules to Include

- Default top/bottom N = 5
- Calendar month vs rolling N days distinction
- Half-open date boundary convention
- ILIKE for all text filters
- Filtered columns must appear in SELECT
- MEASURE() + GROUP BY ALL for metric views
- Percentage format: `CONCAT(ROUND(MEASURE(kpi) * 100, 2), '%')`
