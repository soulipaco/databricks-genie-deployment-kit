#!/usr/bin/env python3
"""
validate.py — Validate the deployment kit structure

Usage:
  python scripts/validate.py
  python scripts/validate.py --output json
"""
import os
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
import yaml

KIT_ROOT = Path(__file__).resolve().parent.parent
ERRORS = []
WARNINGS = []


def error(msg):
    ERRORS.append(msg)


def warn(msg):
    WARNINGS.append(msg)


def load_yaml(path):
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        error(f"Cannot parse YAML {path.name}: {e}")
        return None


def check_required_files():
    required = [
        "room.config.yml",
        "data_sources/tables.yml",
        "instructions/general.md",
        "instruction_library/activation/limits.yml",
    ]
    for rel in required:
        path = KIT_ROOT / rel
        if not path.exists():
            error(f"Missing required file: {rel}")


def check_data_sources():
    tables_file = KIT_ROOT / "data_sources" / "tables.yml"
    if not tables_file.exists():
        return
    data = load_yaml(tables_file)
    if not data or "tables" not in data:
        error("data_sources/tables.yml: missing 'tables' key")
        return
    for table in data.get("tables") or []:
        identifier = table.get("identifier", "")
        parts = identifier.split(".")
        if len(parts) != 3:
            error(f"Table identifier must be 3-level (catalog.schema.table): {identifier}")
        col_meta = table.get("column_metadata_file")
        if col_meta:
            col_path = KIT_ROOT / col_meta
            if not col_path.exists():
                warn(f"Column metadata file missing: {col_meta}")


def check_id_uniqueness(asset_type, directory):
    dir_path = KIT_ROOT / directory
    if not dir_path.exists():
        return
    seen_ids = {}
    for f in sorted(dir_path.glob("*.yml")):
        data = load_yaml(f)
        if not data:
            continue
        id_ = data.get("id")
        if not id_:
            warn(f"{directory}/{f.name}: missing 'id' field")
            continue
        if len(id_) != 32:
            warn(f"{directory}/{f.name}: id should be 32 chars, got {len(id_)}")
        if id_ in seen_ids:
            error(f"Duplicate ID {id_} in {directory}: {f.name} and {seen_ids[id_]}")
        else:
            seen_ids[id_] = f.name


def check_activation_manifests():
    activation = KIT_ROOT / "instruction_library" / "activation"
    for manifest in activation.glob("*.active.yml"):
        data = load_yaml(manifest)
        if not data:
            continue
        ids = data.get("active_ids") or []
        seen = set()
        for id_ in ids:
            if id_ in seen:
                error(f"{manifest.name}: duplicate ID {id_}")
            seen.add(id_)


def check_placeholder_in_env():
    for env_file in (KIT_ROOT / "env").glob("*.yml"):
        with open(env_file) as f:
            content = f.read()
        if "{{" in content:
            warn(f"{env_file.name}: contains unfilled {{{{PLACEHOLDER}}}} values")


def main():
    parser = argparse.ArgumentParser(description="Validate deployment kit structure")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    check_required_files()
    check_data_sources()
    check_id_uniqueness("benchmarks", "benchmarks")
    check_id_uniqueness("example_sql", "instructions/example_sql")
    check_id_uniqueness("filters", "instructions/sql_snippets/filters")
    check_id_uniqueness("measures", "instructions/sql_snippets/measures")
    check_activation_manifests()
    check_placeholder_in_env()

    if args.output == "json":
        result = {"errors": ERRORS, "warnings": WARNINGS, "status": "PASS" if not ERRORS else "FAIL"}
        print(json.dumps(result, indent=2))
    else:
        if ERRORS:
            print(f"ERRORS ({len(ERRORS)}):")
            for e in ERRORS:
                print(f"  ERROR: {e}")
        if WARNINGS:
            print(f"WARNINGS ({len(WARNINGS)}):")
            for w in WARNINGS:
                print(f"  WARN: {w}")
        if not ERRORS and not WARNINGS:
            print("Validation passed: 0 errors, 0 warnings")
        elif not ERRORS:
            print(f"Validation passed with {len(WARNINGS)} warnings")
        else:
            print(f"Validation FAILED: {len(ERRORS)} errors, {len(WARNINGS)} warnings")

    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
