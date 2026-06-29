#!/usr/bin/env python3
"""
pull_room_to_folder.py — Pull a live Genie room into the local folder

Usage:
  python scripts/pull_room_to_folder.py
  python scripts/pull_room_to_folder.py --env prod
  python scripts/pull_room_to_folder.py --dry-run
"""
import os
import sys
import json
import argparse
from pathlib import Path
import yaml
try:
    import requests
except ImportError:
    requests = None

KIT_ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_env(env_name):
    env_path = KIT_ROOT / "env" / f"{env_name}.yml"
    if not env_path.exists():
        raise FileNotFoundError(f"Environment file not found: {env_path}")
    return load_yaml(env_path)


def get_auth():
    try:
        ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
        host = "https://" + ctx.browserHostName().get()
        token = ctx.apiToken().get()
        return host, token
    except Exception:
        host = os.environ.get("DATABRICKS_HOST")
        token = os.environ.get("DATABRICKS_TOKEN")
        if not host or not token:
            raise RuntimeError(
                "Cannot determine auth. Set DATABRICKS_HOST and DATABRICKS_TOKEN "
                "environment variables, or run inside a Databricks notebook."
            )
        return host, token


def unwrap(val):
    if isinstance(val, list) and len(val) == 1:
        return val[0]
    return val


def fetch_room(host, token, space_id):
    if requests is None:
        raise ImportError("requests library required. Install: pip install requests")
    url = f"{host}/api/2.0/genie/spaces/{space_id}?include_serialized_space=true"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()


def write_yaml(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def slugify(text, max_len=50):
    import re
    text = re.sub(r"[^a-z0-9]+", "_", text.lower())
    return text[:max_len].strip("_")


def pull(room_data, dry_run=False):
    serialized = room_data.get("serialized_space")
    if isinstance(serialized, str):
        serialized = json.loads(serialized)

    instructions = serialized.get("instructions", {})
    benchmarks = serialized.get("benchmarks", {})
    config = serialized.get("config", {})

    counts = {}

    text_instructions = instructions.get("text_instructions", [])
    if text_instructions:
        general_path = KIT_ROOT / "instructions" / "general.md"
        general_text = unwrap(text_instructions[0].get("content", [""]))
        if not dry_run:
            general_path.parent.mkdir(parents=True, exist_ok=True)
            general_path.write_text(general_text)
        print(f"  general.md: pulled ({len(general_text)} chars)")

    example_sqls = instructions.get("example_question_sqls", [])
    ex_dir = KIT_ROOT / "instructions" / "example_sql"
    if not dry_run:
        ex_dir.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(example_sqls):
        id_ = item["id"]
        question = unwrap(item.get("question", [""]))
        sql = unwrap(item.get("sql", [""]))
        slug = slugify(question)
        filename = f"{i+1:02d}_{slug}.yml"
        data = {"id": id_, "question": question, "sql": sql}
        params = item.get("parameters", [])
        if params:
            data["parameters"] = [{"name": p["name"], "type_hint": p.get("type_hint", "STRING")} for p in params]
        guidance = item.get("usage_guidance")
        if guidance:
            data["usage_guidance"] = unwrap(guidance)
        if not dry_run:
            write_yaml(ex_dir / filename, data)
    counts["example_sql"] = len(example_sqls)

    sql_snippets = instructions.get("sql_snippets", {})

    filters = sql_snippets.get("filters", [])
    filter_dir = KIT_ROOT / "instructions" / "sql_snippets" / "filters"
    if not dry_run:
        filter_dir.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(filters):
        id_ = item["id"]
        display_name = unwrap(item.get("display_name", [""]))
        sql = unwrap(item.get("sql", [""]))
        slug = slugify(display_name)
        filename = f"{i+1:02d}_{slug}.yml"
        data = {"id": id_, "display_name": display_name, "sql": sql}
        if item.get("synonyms"):
            data["synonyms"] = item["synonyms"]
        if item.get("instruction"):
            data["instruction"] = unwrap(item["instruction"])
        if not dry_run:
            write_yaml(filter_dir / filename, data)
    counts["filters"] = len(filters)

    measures = sql_snippets.get("measures", [])
    measure_dir = KIT_ROOT / "instructions" / "sql_snippets" / "measures"
    if not dry_run:
        measure_dir.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(measures):
        id_ = item["id"]
        alias = item.get("alias", "")
        display_name = unwrap(item.get("display_name", [""]))
        sql = unwrap(item.get("sql", [""]))
        slug = slugify(display_name or alias)
        filename = f"{i+1:02d}_{slug}.yml"
        data = {"id": id_, "alias": alias, "display_name": display_name, "sql": sql}
        if item.get("synonyms"):
            data["synonyms"] = item["synonyms"]
        if item.get("instruction"):
            data["instruction"] = unwrap(item["instruction"])
        if not dry_run:
            write_yaml(measure_dir / filename, data)
    counts["measures"] = len(measures)

    bench_list = benchmarks.get("questions", [])
    bench_dir = KIT_ROOT / "benchmarks"
    if not dry_run:
        bench_dir.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(bench_list):
        id_ = item["id"]
        question = unwrap(item.get("question", [""]))
        answers = item.get("answer", [])
        sql = ""
        fmt = "SQL"
        if answers:
            ans = answers[0] if isinstance(answers, list) else answers
            if isinstance(ans, dict):
                sql = unwrap(ans.get("content", [""]))
                fmt = ans.get("format", "SQL")
        slug = slugify(question)
        filename = f"{i+1:02d}_{slug}.yml"
        data = {"id": id_, "question": question, "answer_format": fmt, "sql": sql}
        if not dry_run:
            write_yaml(bench_dir / filename, data)
    counts["benchmarks"] = len(bench_list)

    return counts


def main():
    parser = argparse.ArgumentParser(description="Pull Genie room into local folder")
    parser.add_argument("--env", default="local", help="Environment name (default: local)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be pulled without writing")
    args = parser.parse_args()

    env = load_env(args.env)
    space_id = env.get("space_id")
    if not space_id:
        print("ERROR: space_id not set in env file. Cannot pull.")
        return 1

    print(f"Pulling from space: {space_id}")
    host, token = get_auth()
    room_data = fetch_room(host, token, space_id)

    counts = pull(room_data, args.dry_run)
    prefix = "[DRY RUN] " if args.dry_run else ""
    for asset_type, count in counts.items():
        print(f"  {prefix}{asset_type}: {count} items pulled")
    print("Pull complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
