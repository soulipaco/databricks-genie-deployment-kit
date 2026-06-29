#!/usr/bin/env python3
"""
analyze_benchmarks.py — Analyze benchmark evaluation results

Usage:
  python scripts/analyze_benchmarks.py --input build/eval_results.yml
  python scripts/analyze_benchmarks.py --input build/eval_results.yml --output-summary
"""
import sys
import argparse
from pathlib import Path
from collections import Counter
import yaml

KIT_ROOT = Path(__file__).resolve().parent.parent

CLASS_NAMES = {
    1: "OUTPUT-SHAPE",
    2: "SEMANTIC-GENERATION",
    3: "BENCHMARK-DEFECT",
    4: "EVALUATOR-FRAGILITY",
    5: "MIXED",
    6: "RETRIEVAL-COLLISION",
    7: "SNIPPET-CONTRADICTION",
}


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Analyze benchmark evaluation results")
    parser.add_argument("--input", required=True, help="Input evaluation results YAML file")
    parser.add_argument("--output-summary", action="store_true", help="Write summary to build/eval_summary.yml")
    args = parser.parse_args()

    input_path = KIT_ROOT / args.input if not Path(args.input).is_absolute() else Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return 1

    results = load_yaml(input_path)
    benchmarks = results.get("results", results.get("failures", []))
    total = results.get("total", len(benchmarks))
    passed = results.get("passed", 0)
    failed = results.get("failed", len([b for b in benchmarks if b.get("status") == "FAIL"]))

    print(f"Benchmark Analysis")
    print(f"  Total: {total} | Passed: {passed} | Failed: {failed}")
    if total > 0:
        print(f"  Pass rate: {passed/total*100:.1f}%")

    class_counts = Counter()
    priority_counts = Counter()

    failures = [b for b in benchmarks if b.get("status") == "FAIL" or b.get("classification")]
    for f in failures:
        cls = f.get("classification", 0)
        if cls:
            class_counts[cls] += 1
        pri = f.get("priority", 0)
        if pri:
            priority_counts[pri] += 1

    if class_counts:
        print("\nFailure Classification:")
        for cls in sorted(class_counts):
            print(f"  Class {cls} ({CLASS_NAMES.get(cls, 'Unknown')}): {class_counts[cls]}")

    if priority_counts:
        print("\nBy Priority:")
        for pri in sorted(priority_counts):
            print(f"  P{pri}: {priority_counts[pri]}")

    if args.output_summary:
        summary = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(passed/total*100, 1) if total > 0 else 0,
            "by_class": dict(class_counts),
            "by_priority": dict(priority_counts),
        }
        summary_path = KIT_ROOT / "build" / "eval_summary.yml"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        with open(summary_path, "w") as f:
            yaml.dump(summary, f, default_flow_style=False)
        print(f"\nSummary written to: {summary_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
