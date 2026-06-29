#!/usr/bin/env python3
"""
Snippet Health Check — Genie Room Deployment Kit

Usage:
  python scripts/snippet_health_check.py --mode full
  python scripts/snippet_health_check.py --mode full --type filters
  python scripts/snippet_health_check.py --mode single --target <alias>
  python scripts/snippet_health_check.py --mode full --fix-plan
  python scripts/snippet_health_check.py --mode full --output json

Checks:
  CHK-1: Exact SQL duplicates
  CHK-2: Alias conflicts (same alias, different SQL)
  CHK-3: Display name conflicts (same display_name, different SQL)
  CHK-4: Non-qualified table references (missing catalog.schema. prefix)
  CHK-5: Wrong date anchor in dimensions (table column instead of CURRENT_DATE)
  CHK-6: MEASURE() vs raw conflict (same alias both ways)
  CHK-7: Convention violations (BETWEEN, dead CASE, missing instruction fields)
"""
import os
import re
import sys
import json
import argparse
from collections import defaultdict
from pathlib import Path
import yaml

_SCRIPT_DIR = Path(__file__).resolve().parent
_KIT_ROOT = _SCRIPT_DIR.parent
SNIPPET_DIRS = {
    "filters": _KIT_ROOT / "instructions" / "sql_snippets" / "filters",
    "measures": _KIT_ROOT / "instructions" / "sql_snippets" / "measures",
    "dimensions": _KIT_ROOT / "instructions" / "sql_snippets" / "dimensions",
    "example_sql": _KIT_ROOT / "instructions" / "example_sql",
}


def load_yaml(path):
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        return None


def normalize_sql(sql):
    if not sql:
        return ""
    sql = re.sub(r"--[^\n]*", "", sql)
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    sql = re.sub(r"\s+", " ", sql).strip().lower()
    return sql


def load_snippets(snippet_type):
    dir_path = SNIPPET_DIRS.get(snippet_type)
    if not dir_path or not dir_path.exists():
        return []
    snippets = []
    for f in sorted(dir_path.glob("*.yml")):
        data = load_yaml(f)
        if data:
            data["_file"] = f.name
            data["_path"] = str(f)
            snippets.append(data)
    return snippets


def chk1_exact_duplicates(snippets):
    issues = []
    sql_to_snippets = defaultdict(list)
    for s in snippets:
        norm = normalize_sql(s.get("sql", ""))
        sql_to_snippets[norm].append(s)
    for norm_sql, group in sql_to_snippets.items():
        if len(group) > 1:
            files = [s["_file"] for s in group]
            issues.append({
                "check": "CHK-1",
                "severity": "HIGH",
                "message": f"Exact SQL duplicate across: {files}",
                "files": files,
                "fix": "Merge instructions, delete duplicates",
            })
    return issues


def chk2_alias_conflicts(snippets):
    issues = []
    alias_to = defaultdict(list)
    for s in snippets:
        alias = s.get("alias")
        if alias:
            norm = normalize_sql(s.get("sql", ""))
            alias_to[alias].append((norm, s["_file"]))
    for alias, entries in alias_to.items():
        unique_sqls = set(e[0] for e in entries)
        if len(unique_sqls) > 1:
            files = [e[1] for e in entries]
            issues.append({
                "check": "CHK-2",
                "severity": "CRITICAL",
                "message": f"Alias conflict: alias '{alias}' has {len(unique_sqls)} different SQL variants in {files}",
                "files": files,
                "fix": "Determine correct SQL; re-alias or retire the wrong variant",
            })
    return issues


def chk3_display_name_conflicts(snippets):
    issues = []
    name_to = defaultdict(list)
    for s in snippets:
        name = s.get("display_name")
        if name:
            norm = normalize_sql(s.get("sql", ""))
            name_to[name].append((norm, s["_file"]))
    for name, entries in name_to.items():
        unique_sqls = set(e[0] for e in entries)
        if len(unique_sqls) > 1:
            files = [e[1] for e in entries]
            issues.append({
                "check": "CHK-3",
                "severity": "HIGH",
                "message": f"Display name conflict: '{name}' has {len(unique_sqls)} different SQL variants",
                "files": files,
                "fix": "Differentiate display names or unify SQL",
            })
    return issues


def chk4_non_qualified_tables(snippets):
    issues = []
    for s in snippets:
        sql = s.get("sql", "")
        if not sql:
            continue
        from_matches = re.findall(r"\bfrom\s+(\S+)", sql, re.IGNORECASE)
        join_matches = re.findall(r"\bjoin\s+(\S+)", sql, re.IGNORECASE)
        for table in from_matches + join_matches:
            table = table.strip("(),")
            if "." not in table and not table.startswith(":") and not table.startswith("("):
                issues.append({
                    "check": "CHK-4",
                    "severity": "MEDIUM",
                    "message": f"{s['_file']}: unqualified table reference '{table}'",
                    "files": [s["_file"]],
                    "fix": f"Prefix with catalog.schema.{table}",
                })
    return issues


def chk5_wrong_date_anchor(snippets, snippet_type):
    issues = []
    if snippet_type != "dimensions":
        return issues
    for s in snippets:
        sql = s.get("sql", "")
        if not sql:
            continue
        alias = s.get("alias", s["_file"])
        date_col_pattern = re.search(r"\b(date|created_at|updated_at|event_date)\b", sql, re.IGNORECASE)
        current_date_pattern = re.search(r"current_date|current_timestamp|date_trunc|date_sub|date_add", sql, re.IGNORECASE)
        if date_col_pattern and not current_date_pattern:
            issues.append({
                "check": "CHK-5",
                "severity": "HIGH",
                "message": f"{s['_file']}: dimension '{alias}' may use table date column instead of CURRENT_DATE()",
                "files": [s["_file"]],
                "fix": "Replace table date column reference with CURRENT_DATE() expression",
            })
    return issues


def chk6_measure_vs_raw(all_snippets_by_type):
    issues = []
    alias_has_measure = defaultdict(list)
    alias_has_raw = defaultdict(list)
    for stype, snippets in all_snippets_by_type.items():
        for s in snippets:
            alias = s.get("alias")
            sql = s.get("sql", "")
            if not alias or not sql:
                continue
            if re.search(r"\bMEASURE\s*\(", sql, re.IGNORECASE):
                alias_has_measure[alias].append((stype, s["_file"]))
            else:
                alias_has_raw[alias].append((stype, s["_file"]))
    for alias in alias_has_measure:
        if alias in alias_has_raw:
            m_files = [f[1] for f in alias_has_measure[alias]]
            r_files = [f[1] for f in alias_has_raw[alias]]
            issues.append({
                "check": "CHK-6",
                "severity": "HIGH",
                "message": f"Alias '{alias}' has MEASURE() version ({m_files}) AND raw version ({r_files})",
                "files": m_files + r_files,
                "fix": "Keep MEASURE() version; retire raw unless non-aggregation context needed",
            })
    return issues


def chk7_convention_violations(snippets, snippet_type):
    issues = []
    for s in snippets:
        sql = s.get("sql", "")
        f = s["_file"]
        if re.search(r"\bBETWEEN\b", sql, re.IGNORECASE):
            issues.append({
                "check": "CHK-7a",
                "severity": "LOW",
                "message": f"{f}: uses BETWEEN for date range (prefer half-open >= AND <)",
                "files": [f],
                "fix": "Replace BETWEEN with >= start AND < end_exclusive",
            })
        if re.search(r"\bWHEN\s+1\s*=\s*1\b|\bWHEN\s+TRUE\b|\bWHEN\s+'a'\s*=\s*'a'", sql, re.IGNORECASE):
            issues.append({
                "check": "CHK-7c",
                "severity": "LOW",
                "message": f"{f}: dead-code CASE logic (always-true WHEN condition)",
                "files": [f],
                "fix": "Remove dead CASE branch",
            })
        instruction = s.get("instruction", "")
        if snippet_type in ("filters", "measures") and instruction:
            if "WHEN_TO_USE" not in instruction:
                issues.append({
                    "check": "CHK-7d",
                    "severity": "LOW",
                    "message": f"{f}: instruction missing WHEN_TO_USE field",
                    "files": [f],
                    "fix": "Add WHEN_TO_USE line to instruction field",
                })
    return issues


def run_checks(target_types, target_alias=None):
    all_issues = []
    all_snippets_by_type = {}
    for stype in target_types:
        snippets = load_snippets(stype)
        if target_alias:
            snippets = [s for s in snippets if s.get("alias") == target_alias or target_alias in s.get("_file", "")]
        all_snippets_by_type[stype] = snippets
        all_issues.extend(chk1_exact_duplicates(snippets))
        all_issues.extend(chk2_alias_conflicts(snippets))
        all_issues.extend(chk3_display_name_conflicts(snippets))
        all_issues.extend(chk4_non_qualified_tables(snippets))
        all_issues.extend(chk5_wrong_date_anchor(snippets, stype))
        all_issues.extend(chk7_convention_violations(snippets, stype))
    all_issues.extend(chk6_measure_vs_raw(all_snippets_by_type))
    return all_issues


def main():
    parser = argparse.ArgumentParser(description="Snippet health check for Genie deployment kit")
    parser.add_argument("--mode", choices=["full", "single"], default="full")
    parser.add_argument("--type", choices=["filters", "measures", "dimensions", "example_sql"])
    parser.add_argument("--target", help="Alias or filename substring for --mode single")
    parser.add_argument("--fix-plan", action="store_true", help="Include fix suggestions in output")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    target_types = [args.type] if args.type else list(SNIPPET_DIRS.keys())
    target_alias = args.target if args.mode == "single" else None

    issues = run_checks(target_types, target_alias)

    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    issues.sort(key=lambda x: severity_order.get(x.get("severity", "LOW"), 3))

    if args.output == "json":
        print(json.dumps({"issues": issues, "total": len(issues)}, indent=2))
    else:
        if not issues:
            print("Snippet Health Check: PASS (0 issues)")
        else:
            print(f"Snippet Health Check: {len(issues)} issues found")
            for issue in issues:
                sev = issue.get("severity", "??")
                print(f"  [{sev}] {issue['check']}: {issue['message']}")
                if args.fix_plan:
                    print(f"    Fix: {issue.get('fix', '(no fix suggestion)')}")

    return 1 if any(i.get("severity") in ("CRITICAL", "HIGH") for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
