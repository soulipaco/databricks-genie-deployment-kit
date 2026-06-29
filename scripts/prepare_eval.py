#!/usr/bin/env python3
"""
prepare_eval.py — Prepare benchmark evaluation batch

Usage:
  python scripts/prepare_eval.py
  python scripts/prepare_eval.py --output build/eval_batch.yml
  python scripts/prepare_eval.py --check-only
"""
import sys
import argparse
from pathlib import Path
import yaml

KIT_ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Prepare benchmark evaluation batch")
    parser.add_argument("--output", default="build/eval_batch.yml", help="Output file path")
    parser.add_argument("--check-only", action="store_true", help="Report readiness without writing")
    args = parser.parse_args()

    bench_dir = KIT_ROOT / "benchmarks"
    if not bench_dir.exists():
        print("ERROR: benchmarks/ directory not found")
        return 1

    benchmarks = []
    for f in sorted(bench_dir.glob("*.yml")):
        try:
            data = load_yaml(f)
            if data:
                benchmarks.append({"id": data["id"], "question": data["question"], "gt_sql": data.get("sql", "")})
        except Exception as e:
            print(f"  WARN: Cannot parse {f.name}: {e}")

    if not benchmarks:
        print("WARNING: No benchmarks found")
        return 0

    instructions_ok = (KIT_ROOT / "instructions" / "general.md").exists()
    example_sql_count = len(list((KIT_ROOT / "instructions" / "example_sql").glob("*.yml")))
    filter_count = len(list((KIT_ROOT / "instructions" / "sql_snippets" / "filters").glob("*.yml")))
    measure_count = len(list((KIT_ROOT / "instructions" / "sql_snippets" / "measures").glob("*.yml")))

    status = "READY" if instructions_ok else "NOT_READY"

    print(f"Evaluation Readiness: {status}")
    print(f"  Benchmarks: {len(benchmarks)}")
    print(f"  General instructions: {'OK' if instructions_ok else 'MISSING'}")
    print(f"  Example SQL: {example_sql_count}")
    print(f"  Filters: {filter_count}")
    print(f"  Measures: {measure_count}")

    if args.check_only:
        return 0 if status == "READY" else 1

    batch = {
        "readiness": status,
        "benchmark_count": len(benchmarks),
        "benchmarks": benchmarks,
    }

    output_path = KIT_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(batch, f, default_flow_style=False, allow_unicode=True)
    print(f"Batch written to: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
