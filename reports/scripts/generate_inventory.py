#!/usr/bin/env python3
"""
generate_inventory.py — Auto-generate JSON inventory data files from the Genie Room Deployment Kit

Scans the kit structure and produces 7 JSON data files in reports/data/:
  - room_identity.json         Room metadata, capacity, environment
  - domain_capabilities.json   All example SQL with parameters and usage_guidance
  - benchmark_inventory.json   All benchmark test cases with status
  - snippet_inventory.json     All filters, measures, dimensions
  - evaluation_history.json    Evaluation results (reads build/eval_*.yml)
  - sales_ready_questions.json Question catalog with business mapping
  - data_sources.json          Full schema reference

Also generates stub markdown summaries in reports/summaries/ if they do not exist.

Usage:
  python reports/scripts/generate_inventory.py
  python reports/scripts/generate_inventory.py --no-summaries
  python reports/scripts/generate_inventory.py --output-dir reports/data
"""
import os
import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
import yaml

_SCRIPT_DIR = Path(__file__).resolve().parent   # reports/scripts/
_KIT_ROOT = _SCRIPT_DIR.parent.parent           # kit root
DATA_DIR = _SCRIPT_DIR.parent / "data"
SUMMARIES_DIR = _SCRIPT_DIR.parent / "summaries"


def load_yaml(path):
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"  WARN: Cannot parse {path.name}: {e}")
        return None


def load_all_yaml_in(directory):
    dir_path = _KIT_ROOT / directory
    results = []
    if not dir_path.exists():
        return results
    for f in sorted(dir_path.glob("*.yml")):
        data = load_yaml(f)
        if data:
            data["_source_file"] = f.name
            results.append(data)
    return results


def generate_room_identity():
    """Read room.config.yml and env/ to produce room_identity.json."""
    config = load_yaml(_KIT_ROOT / "room.config.yml") or {}
    env_local = load_yaml(_KIT_ROOT / "env" / "local.yml") or {}
    limits = load_yaml(_KIT_ROOT / "instruction_library" / "activation" / "limits.yml") or {}
    tables = load_yaml(_KIT_ROOT / "data_sources" / "tables.yml") or {}
    table_count = len((tables.get("tables") or []))
    total = limits.get("max_total_space_instructions", 100)
    general = limits.get("general_text_instruction_count", 1)
    example_sql_budget = total - general - table_count

    ex_sql_count = len(list((_KIT_ROOT / "instructions" / "example_sql").glob("*.yml")))
    filter_count = len(list((_KIT_ROOT / "instructions" / "sql_snippets" / "filters").glob("*.yml")))
    measure_count = len(list((_KIT_ROOT / "instructions" / "sql_snippets" / "measures").glob("*.yml")))
    bench_count = len(list((_KIT_ROOT / "benchmarks").glob("*.yml")))

    return {
        "room_name": config.get("room_name", ""),
        "title": config.get("title", ""),
        "description": config.get("description", ""),
        "version": config.get("version", 2),
        "workspace_url": env_local.get("workspace_url", ""),
        "warehouse_id": env_local.get("warehouse_id", ""),
        "space_id": env_local.get("space_id", ""),
        "parent_path": config.get("parent_path", ""),
        "capacity": {
            "max_total_space_instructions": total,
            "general_text_instruction_count": general,
            "table_description_count": table_count,
            "example_sql_budget": example_sql_budget,
        },
        "asset_counts": {
            "example_sql_active": ex_sql_count,
            "filters_active": filter_count,
            "measures_active": measure_count,
            "benchmarks": bench_count,
            "tables": table_count,
        },
        "sample_questions": [
            q.get("question", "") for q in (config.get("sample_questions") or [])
        ],
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def generate_domain_capabilities():
    """Read all active example_sql to produce domain_capabilities.json."""
    items = load_all_yaml_in("instructions/example_sql")
    capabilities = []
    for item in items:
        cap = {
            "id": item.get("id", ""),
            "question": item.get("question", ""),
            "sql": item.get("sql", ""),
            "source_file": item.get("_source_file", ""),
        }
        if item.get("parameters"):
            cap["parameters"] = item["parameters"]
        if item.get("usage_guidance"):
            cap["usage_guidance"] = item["usage_guidance"]
        capabilities.append(cap)
    return {
        "total": len(capabilities),
        "capabilities": capabilities,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def generate_benchmark_inventory():
    """Read all benchmarks/ to produce benchmark_inventory.json."""
    items = load_all_yaml_in("benchmarks")
    benchmarks = []
    for item in items:
        bench = {
            "id": item.get("id", ""),
            "question": item.get("question", ""),
            "answer_format": item.get("answer_format", "SQL"),
            "sql": item.get("sql", ""),
            "source_file": item.get("_source_file", ""),
        }
        cleanup = item.get("_cleanup_flags")
        if cleanup:
            bench["cleanup_flags"] = cleanup
            bench["status"] = "needs_cleanup"
        else:
            bench["status"] = "clean"
        benchmarks.append(bench)
    return {
        "total": len(benchmarks),
        "clean": len([b for b in benchmarks if b["status"] == "clean"]),
        "needs_cleanup": len([b for b in benchmarks if b["status"] == "needs_cleanup"]),
        "benchmarks": benchmarks,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def generate_snippet_inventory():
    """Read all active snippets to produce snippet_inventory.json."""
    filters = load_all_yaml_in("instructions/sql_snippets/filters")
    measures = load_all_yaml_in("instructions/sql_snippets/measures")
    dimensions = load_all_yaml_in("instructions/sql_snippets/dimensions")

    def clean(items, type_):
        out = []
        for item in items:
            entry = {
                "id": item.get("id", ""),
                "type": type_,
                "display_name": item.get("display_name", item.get("alias", "")),
                "sql": item.get("sql", ""),
                "source_file": item.get("_source_file", ""),
            }
            if item.get("alias"):
                entry["alias"] = item["alias"]
            if item.get("synonyms"):
                entry["synonyms"] = item["synonyms"]
            if item.get("instruction"):
                entry["has_instruction"] = True
            out.append(entry)
        return out

    all_snippets = clean(filters, "filter") + clean(measures, "measure") + clean(dimensions, "dimension")
    return {
        "total": len(all_snippets),
        "by_type": {
            "filters": len(filters),
            "measures": len(measures),
            "dimensions": len(dimensions),
        },
        "snippets": all_snippets,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def generate_data_sources():
    """Read data_sources/tables.yml and column metadata to produce data_sources.json."""
    tables_config = load_yaml(_KIT_ROOT / "data_sources" / "tables.yml") or {}
    tables = []
    for table in (tables_config.get("tables") or []):
        entry = {
            "identifier": table.get("identifier", ""),
            "description": table.get("description", ""),
            "column_metadata_file": table.get("column_metadata_file", ""),
        }
        col_meta_path = _KIT_ROOT / (table.get("column_metadata_file", ""))
        if col_meta_path.exists():
            col_meta = load_yaml(col_meta_path) or {}
            cols = col_meta.get("columns") or []
            entry["columns"] = [
                {
                    "column_name": c.get("column_name", ""),
                    "exclude": c.get("exclude", False),
                    "enable_entity_matching": c.get("enable_entity_matching", False),
                    "get_example_values": c.get("get_example_values", False),
                    "build_value_dictionary": c.get("build_value_dictionary", False),
                    "enable_format_assistance": c.get("enable_format_assistance", False),
                }
                for c in cols
            ]
            entry["column_count"] = len(cols)
        tables.append(entry)
    return {
        "total_tables": len(tables),
        "tables": tables,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def generate_evaluation_history():
    """Read build/eval_*.yml files to produce evaluation_history.json."""
    build_dir = _KIT_ROOT / "build"
    sessions = []
    if build_dir.exists():
        for f in sorted(build_dir.glob("eval_*.yml")):
            data = load_yaml(f)
            if data:
                sessions.append({
                    "source_file": f.name,
                    "total": data.get("total", 0),
                    "passed": data.get("passed", 0),
                    "failed": data.get("failed", 0),
                    "pass_rate": data.get("pass_rate", None),
                    "failures": data.get("failures", []),
                })
    total_evaluated = sum(s.get("total", 0) for s in sessions)
    total_passed = sum(s.get("passed", 0) for s in sessions)
    total_failed = sum(s.get("failed", 0) for s in sessions)
    return {
        "sessions": len(sessions),
        "total_evaluated": total_evaluated,
        "total_passed": total_passed,
        "total_failed": total_failed,
        "overall_pass_rate": round(total_passed / total_evaluated * 100, 1) if total_evaluated > 0 else None,
        "history": sessions,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def generate_sales_ready_questions():
    """Read example_sql with usage_guidance to produce sales_ready_questions.json."""
    items = load_all_yaml_in("instructions/example_sql")
    questions = []
    for item in items:
        q = {
            "id": item.get("id", ""),
            "question": item.get("question", ""),
            "source_file": item.get("_source_file", ""),
        }
        if item.get("parameters"):
            q["parameters"] = [p.get("name", "") for p in item.get("parameters", [])]
        if item.get("usage_guidance"):
            guidance = item["usage_guidance"]
            trigger_match = re.search(r"TRIGGER PHRASES:(.*?)(?=DATE BINDING:|MANDATORY|$)", guidance, re.DOTALL)
            if trigger_match:
                q["trigger_phrases"] = trigger_match.group(1).strip()
        questions.append(q)
    return {
        "total": len(questions),
        "questions": questions,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def write_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return len(json.dumps(data))


def generate_summary_stubs(room_identity, capabilities, benchmarks, snippets, data_sources, eval_history):
    """Generate starter markdown summaries if they do not already exist."""
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
    room_name = room_identity.get("room_name", "{{ROOM_NAME}}")
    title = room_identity.get("title", room_name)
    n_examples = capabilities.get("total", 0)
    n_benchmarks = benchmarks.get("total", 0)
    n_snippets = snippets.get("total", 0)
    n_tables = data_sources.get("total_tables", 0)
    n_filters = snippets.get("by_type", {}).get("filters", 0)
    n_measures = snippets.get("by_type", {}).get("measures", 0)
    n_dimensions = snippets.get("by_type", {}).get("dimensions", 0)
    n_sessions = eval_history.get("sessions", 0)
    n_evaluated = eval_history.get("total_evaluated", 0)
    pass_rate = eval_history.get("overall_pass_rate")
    today = datetime.utcnow().strftime("%Y-%m-%d")

    files = {
        "00_sales_ready_overview.md": f"""# {title} — Sales-Ready Capability Overview

> **Room:** `{room_name}` | **Report date:** {today} | **Source of truth:** repo

## At-a-Glance Capability Matrix

| Metric | Count |
|--------|-------|
| Example SQL Templates | {n_examples} |
| Benchmark Test Cases | {n_benchmarks} |
| SQL Snippets | {n_snippets} ({n_filters} filters, {n_measures} measures, {n_dimensions} dimensions) |
| Data Sources (Metric Views) | {n_tables} |

## What This Room Answers

This room enables natural-language questions across:

<!-- Add per-domain capability summary here -->

## Question Catalog

<!-- Auto-populated from domain_capabilities.json -->

See `reports/data/domain_capabilities.json` for the complete list of {n_examples} trained question templates.

## Health Metrics

- **Templates trained:** {n_examples}
- **Benchmarks proven:** {n_benchmarks}
- **SQL snippets:** {n_snippets}
- **Data sources:** {n_tables}
- **Evaluation sessions:** {n_sessions}
""",
        "01_executive_summary.md": f"""# Executive Summary — {title}

> **Report date:** {today} | **Room:** `{room_name}`

## Room Overview

{room_identity.get("description", "<!-- Add room description here -->")}

## Health At-a-Glance

| Asset | Count |
|-------|-------|
| Example SQL Templates | {n_examples} |
| Benchmark Test Cases | {n_benchmarks} |
| SQL Snippets | {n_snippets} |
| Data Sources | {n_tables} |
| Evaluation Sessions | {n_sessions} |
| Total Questions Evaluated | {n_evaluated} |
{f"| Overall Pass Rate | {pass_rate}% |" if pass_rate else ""}

## Operational Status

- Room is {"deployed and operational" if room_identity.get("space_id") else "pending first deployment"}
- Benchmark coverage: {n_benchmarks} ground-truth test cases
- Evaluation status: {"In progress" if n_sessions > 0 else "Not yet started"}

## Next Steps

<!-- Add current priorities and next steps here -->
""",
        "02_domain_capabilities.md": f"""# Domain Capabilities — {title}

> **Report date:** {today} | {n_examples} trained question templates

## Data Sources

""" + "\n".join([
    f"### {t.get('identifier', '')}\n- **Description:** {t.get('description', '')}\n- **Columns:** {t.get('column_count', '?')}\n"
    for t in data_sources.get("tables", [])
]) + f"""\n## Question Templates\n\nSee `reports/data/domain_capabilities.json` for all {n_examples} templates with full SQL.\n""",
        "03_benchmark_coverage.md": f"""# Benchmark Coverage — {title}

> **Report date:** {today} | {n_benchmarks} ground-truth test cases

## Summary

| Status | Count |
|--------|-------|
| Clean | {benchmarks.get("clean", 0)} |
| Needs cleanup | {benchmarks.get("needs_cleanup", 0)} |
| **Total** | **{n_benchmarks}** |

## Benchmark List

See `reports/data/benchmark_inventory.json` for the complete list.\n
""" + "\n".join([
    f"- `{b.get('source_file', '')}` — {b.get('question', '')} ({b.get('status', '')})"
    for b in benchmarks.get("benchmarks", [])
]),
        "04_evaluation_progress.md": f"""# Evaluation Progress — {title}

> **Report date:** {today} | {n_sessions} evaluation session(s)

## Summary

| Metric | Value |
|--------|-------|
| Sessions | {n_sessions} |
| Total Evaluated | {n_evaluated} |
{f"| Overall Pass Rate | {pass_rate}% |" if pass_rate else ""}

## Failure Mode Taxonomy

See `geniecode/BENCHMARK_WORKSPACE.md` for the 7-class failure taxonomy.

## Session History

See `reports/data/evaluation_history.json` for detailed session data.\n
<!-- Add narrative about evaluation sessions here -->
""",
        "05_data_source_reference.md": f"""# Data Source Reference — {title}

> **Report date:** {today} | {n_tables} metric view(s)

""" + "\n".join([
    f"""## {t.get("identifier", "")}

**Description:** {t.get("description", "")}

**Column count:** {t.get("column_count", "?")}

"""
    for t in data_sources.get("tables", [])
]),
        "06_fix_history_and_patterns.md": f"""# Fix History and Patterns — {title}

> **Report date:** {today} | See `geniecode/FIX_PATTERNS.md` for the full pattern library

## Engineering Summary

<!-- Add summary of engineering work done here -->

## Fix Sessions

<!-- Add per-session fix logs here. Format:
### Session: YYYY-MM-DD
- Fixed: ...
- Added: ...
- Removed: ...
-->

## Discovered Patterns

See `geniecode/FIX_PATTERNS.md` for the complete pattern library.
""",
    }

    written = []
    for fname, content in files.items():
        path = SUMMARIES_DIR / fname
        if not path.exists():
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            written.append(fname)
        else:
            print(f"  SKIP (exists): {fname}")
    return written


def main():
    parser = argparse.ArgumentParser(description="Generate JSON inventory data from Genie Deployment Kit")
    parser.add_argument("--output-dir", default=str(DATA_DIR), help="Output directory for JSON files")
    parser.add_argument("--no-summaries", action="store_true", help="Skip generating markdown summary stubs")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating inventory from: {_KIT_ROOT}")
    print(f"Output directory: {output_dir}")
    print()

    generators = [
        ("room_identity.json", generate_room_identity),
        ("domain_capabilities.json", generate_domain_capabilities),
        ("benchmark_inventory.json", generate_benchmark_inventory),
        ("snippet_inventory.json", generate_snippet_inventory),
        ("data_sources.json", generate_data_sources),
        ("evaluation_history.json", generate_evaluation_history),
        ("sales_ready_questions.json", generate_sales_ready_questions),
    ]

    results = {}
    for filename, gen_fn in generators:
        print(f"  Generating {filename}...")
        try:
            data = gen_fn()
            size = write_json(data, output_dir / filename)
            results[filename] = data
            print(f"    OK ({size} bytes)")
        except Exception as e:
            print(f"    ERROR: {e}")
            results[filename] = {}

    if not args.no_summaries:
        print()
        print("  Generating markdown summary stubs...")
        written = generate_summary_stubs(
            results.get("room_identity.json", {}),
            results.get("domain_capabilities.json", {}),
            results.get("benchmark_inventory.json", {}),
            results.get("snippet_inventory.json", {}),
            results.get("data_sources.json", {}),
            results.get("evaluation_history.json", {}),
        )
        if written:
            print(f"    Created: {written}")

    print()
    print("Inventory generation complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
