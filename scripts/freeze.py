#!/usr/bin/env python3
"""
freeze.py — Snapshot current instruction state

Usage:
  python scripts/freeze.py
  python scripts/freeze.py --label before_v2
"""
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import yaml

KIT_ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_all_yaml_in(directory):
    dir_path = KIT_ROOT / directory
    results = []
    if not dir_path.exists():
        return results
    for f in sorted(dir_path.glob("*.yml")):
        try:
            data = load_yaml(f)
            if data:
                results.append(data)
        except Exception:
            pass
    return results


def main():
    parser = argparse.ArgumentParser(description="Snapshot current instruction state")
    parser.add_argument("--label", default="", help="Optional label suffix for the snapshot file")
    args = parser.parse_args()

    now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    label = f"_{args.label}" if args.label else ""
    snapshot_name = f"snapshot_{now}{label}.json"
    snapshot_path = KIT_ROOT / "snapshots" / snapshot_name
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)

    general_path = KIT_ROOT / "instructions" / "general.md"
    general_text = general_path.read_text() if general_path.exists() else ""

    snapshot = {
        "timestamp": now,
        "label": args.label or None,
        "general_instruction": general_text,
        "example_sql": load_all_yaml_in("instructions/example_sql"),
        "filters": load_all_yaml_in("instructions/sql_snippets/filters"),
        "measures": load_all_yaml_in("instructions/sql_snippets/measures"),
        "benchmarks": load_all_yaml_in("benchmarks"),
    }

    counts = {
        "example_sql": len(snapshot["example_sql"]),
        "filters": len(snapshot["filters"]),
        "measures": len(snapshot["measures"]),
        "benchmarks": len(snapshot["benchmarks"]),
    }

    with open(snapshot_path, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Snapshot written: {snapshot_path}")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
