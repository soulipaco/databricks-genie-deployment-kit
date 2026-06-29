#!/usr/bin/env python3
"""
materialize.py — Materialize instruction_library/ into instructions/

Usage:
  python scripts/materialize.py
  python scripts/materialize.py --check-limits
  python scripts/materialize.py --dry-run
"""
import os
import sys
import shutil
import argparse
from pathlib import Path
import yaml

KIT_ROOT = Path(__file__).resolve().parent.parent
LIBRARY = KIT_ROOT / "instruction_library"
ACTIVATION = LIBRARY / "activation"
CORPUS = LIBRARY / "corpus"
INSTRUCTIONS = KIT_ROOT / "instructions"
SNIPPETS = INSTRUCTIONS / "sql_snippets"


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_limits():
    limits_path = ACTIVATION / "limits.yml"
    if not limits_path.exists():
        return {}
    return load_yaml(limits_path)


def load_active_ids(asset_type):
    manifest_path = ACTIVATION / f"{asset_type}.active.yml"
    if not manifest_path.exists():
        return []
    data = load_yaml(manifest_path)
    if data and "active_ids" in data:
        return data["active_ids"] or []
    return []


def load_corpus_index(asset_type):
    corpus_dir = CORPUS / asset_type
    if not corpus_dir.exists():
        return {}
    index = {}
    for f in corpus_dir.glob("*.yml"):
        try:
            data = load_yaml(f)
            if data and "id" in data:
                index[data["id"]] = (f, data)
        except Exception as e:
            print(f"  WARN: Cannot parse {f.name}: {e}")
    return index


def count_tables():
    tables_file = KIT_ROOT / "data_sources" / "tables.yml"
    if not tables_file.exists():
        return 0
    data = load_yaml(tables_file)
    if data and "tables" in data:
        return len(data["tables"] or [])
    return 0


def check_limits(active_counts, limits):
    errors = []
    total = limits.get("max_total_space_instructions", 100)
    general = limits.get("general_text_instruction_count", 1)
    tables = count_tables()
    budgets = limits.get("active_budgets", {})

    example_sql_budget = budgets.get("example_sql", {})
    if example_sql_budget.get("mode") == "derived_total_minus_general_minus_tables":
        example_sql_max = total - general - tables
    else:
        example_sql_max = total - general - tables

    if active_counts.get("example_sql", 0) > example_sql_max:
        errors.append(
            f"example_sql: {active_counts['example_sql']} active > budget {example_sql_max} (total={total} - general={general} - tables={tables})"
        )

    for asset_type in ["filters", "measures"]:
        cap = budgets.get(asset_type, {}).get("max_active", 100)
        if active_counts.get(asset_type, 0) > cap:
            errors.append(f"{asset_type}: {active_counts[asset_type]} active > max_active {cap}")

    return errors


def materialize_type(asset_type, output_dir, active_ids, corpus_index, dry_run=False):
    output_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    missing = []

    if not dry_run:
        for existing in output_dir.glob("*.yml"):
            existing.unlink()

    for id_ in active_ids:
        if id_ in corpus_index:
            src_path, _ = corpus_index[id_]
            dst_path = output_dir / src_path.name
            if not dry_run:
                shutil.copy2(src_path, dst_path)
            copied += 1
        else:
            missing.append(id_)

    return copied, missing


def main():
    parser = argparse.ArgumentParser(description="Materialize instruction_library into instructions/")
    parser.add_argument("--check-limits", action="store_true", help="Check capacity limits and report")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without writing files")
    args = parser.parse_args()

    print(f"Materializing {LIBRARY} -> {INSTRUCTIONS}")

    limits = load_limits()
    active_counts = {}
    total_missing = []

    asset_types = [
        ("filters", SNIPPETS / "filters"),
        ("measures", SNIPPETS / "measures"),
        ("example_sql", INSTRUCTIONS / "example_sql"),
    ]

    for asset_type, output_dir in asset_types:
        active_ids = load_active_ids(asset_type)
        corpus_index = load_corpus_index(asset_type)
        copied, missing = materialize_type(asset_type, output_dir, active_ids, corpus_index, args.dry_run)
        active_counts[asset_type] = copied
        total_missing.extend([(asset_type, id_) for id_ in missing])
        prefix = "[DRY RUN] " if args.dry_run else ""
        print(f"  {prefix}{asset_type}: {copied} active ({len(active_ids)} in manifest, {len(missing)} missing from corpus)")

    if total_missing:
        print("\nWARNING: IDs in activation manifests not found in corpus:")
        for asset_type, id_ in total_missing:
            print(f"  {asset_type}: {id_}")

    if args.check_limits:
        print("\nCapacity Check:")
        limit_errors = check_limits(active_counts, limits)
        total = limits.get("max_total_space_instructions", 100)
        general = limits.get("general_text_instruction_count", 1)
        tables = count_tables()
        example_sql_max = total - general - tables
        print(f"  Total budget:          {total}")
        print(f"  General instruction:   -{general}")
        print(f"  Table descriptions:    -{tables}")
        print(f"  Example SQL budget:    {example_sql_max}")
        print(f"  Example SQL active:    {active_counts.get('example_sql', 0)}")
        print(f"  Filters active:        {active_counts.get('filters', 0)} (cap: 100)")
        print(f"  Measures active:       {active_counts.get('measures', 0)} (cap: 100)")
        if limit_errors:
            print("\nCAPACITY ERRORS:")
            for err in limit_errors:
                print(f"  ERROR: {err}")
            sys.exit(1)
        else:
            print("  Status: OK")

    print("\nMaterialization complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
