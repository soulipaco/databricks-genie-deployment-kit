#!/usr/bin/env python3
"""
push_folder_to_room.py — Deploy local folder to a Genie room via API

Usage:
  python scripts/push_folder_to_room.py
  python scripts/push_folder_to_room.py --env prod
  python scripts/push_folder_to_room.py --dry-run

Note: When running inside a Databricks notebook, authentication is handled
automatically via dbutils. Outside Databricks, set DATABRICKS_HOST and
DATABRICKS_TOKEN environment variables.
"""
import os
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
import yaml
try:
    import requests
except ImportError:
    requests = None

KIT_ROOT = Path(__file__).resolve().parent.parent

TYPE_HINT_MAP = {
    "INT": "INTEGER",
    "FLOAT": "DOUBLE",
    "BOOL": "BOOLEAN",
    "STR": "STRING",
}


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


def normalize_type_hint(hint):
    return TYPE_HINT_MAP.get(hint.upper() if hint else "", hint)


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
        except Exception as e:
            print(f"  WARN: Cannot parse {f.name}: {e}")
    return results


def validate():
    errors = []
    required = [
        "room.config.yml",
        "data_sources/tables.yml",
        "instructions/general.md",
    ]
    for rel in required:
        if not (KIT_ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    example_sqls = load_all_yaml_in("instructions/example_sql")
    ids_seen = {}
    for item in example_sqls:
        id_ = item.get("id")
        if id_ in ids_seen:
            errors.append(f"Duplicate example_sql id: {id_}")
        ids_seen[id_] = True

    benchmarks = load_all_yaml_in("benchmarks")
    bench_ids = {}
    for item in benchmarks:
        id_ = item.get("id")
        if id_ in bench_ids:
            errors.append(f"Duplicate benchmark id: {id_}")
        bench_ids[id_] = True

    return errors


def assemble_payload(env):
    room_config = load_yaml(KIT_ROOT / "room.config.yml")
    tables_config = load_yaml(KIT_ROOT / "data_sources" / "tables.yml")

    with open(KIT_ROOT / "instructions" / "general.md") as f:
        general_text = f.read()

    example_sqls = load_all_yaml_in("instructions/example_sql")
    filters = load_all_yaml_in("instructions/sql_snippets/filters")
    measures = load_all_yaml_in("instructions/sql_snippets/measures")
    benchmarks = load_all_yaml_in("benchmarks")
    sample_questions = room_config.get("sample_questions") or []

    column_metadata_dir = KIT_ROOT / "metadata" / "columns"

    tables_payload = []
    for table in (tables_config.get("tables") or []):
        col_configs = []
        col_meta_file = table.get("column_metadata_file")
        if col_meta_file:
            col_meta_path = KIT_ROOT / col_meta_file
            if col_meta_path.exists():
                col_meta = load_yaml(col_meta_path)
                for col in (col_meta.get("columns") or []):
                    col_entry = {"column_name": col["column_name"]}
                    for flag in ["exclude", "enable_format_assistance", "enable_entity_matching",
                                 "get_example_values", "build_value_dictionary"]:
                        if flag in col:
                            col_entry[flag] = col[flag]
                    col_configs.append(col_entry)
        tables_payload.append({
            "identifier": table["identifier"],
            "description": [table.get("description", "")],
            "column_configs": col_configs,
        })

    import uuid
    general_id = str(uuid.uuid4()).replace("-", "")

    text_instructions = [{"id": general_id, "content": [general_text]}]

    def build_example_sql(item):
        params = []
        for p in (item.get("parameters") or []):
            params.append({"name": p["name"], "type_hint": normalize_type_hint(p.get("type_hint", "STRING"))})
        entry = {
            "id": item["id"],
            "question": [item["question"]],
            "sql": [item["sql"]],
        }
        if params:
            entry["parameters"] = params
        if item.get("usage_guidance"):
            entry["usage_guidance"] = [item["usage_guidance"]]
        return entry

    def build_filter(item):
        entry = {
            "id": item["id"],
            "display_name": [item.get("display_name", "")],
            "sql": [item["sql"]],
        }
        if item.get("synonyms"):
            entry["synonyms"] = item["synonyms"]
        if item.get("instruction"):
            entry["instruction"] = [item["instruction"]]
        return entry

    def build_measure(item):
        entry = {
            "id": item["id"],
            "alias": item.get("alias", ""),
            "display_name": [item.get("display_name", "")],
            "sql": [item["sql"]],
        }
        if item.get("synonyms"):
            entry["synonyms"] = item["synonyms"]
        if item.get("instruction"):
            entry["instruction"] = [item["instruction"]]
        return entry

    def build_benchmark(item):
        return {
            "id": item["id"],
            "question": [item["question"]],
            "answer": [{"format": item.get("answer_format", "SQL"), "content": [item.get("sql", "")]}],
        }

    def build_sample_question(item):
        return {"id": item["id"], "question": [item["question"]]}

    serialized_space = {
        "version": 2,
        "config": {
            "sample_questions": sorted(
                [build_sample_question(q) for q in sample_questions], key=lambda x: x["id"]
            )
        },
        "data_sources": {"tables": sorted(tables_payload, key=lambda x: x["identifier"])},
        "instructions": {
            "text_instructions": text_instructions,
            "example_question_sqls": sorted(
                [build_example_sql(e) for e in example_sqls], key=lambda x: x["id"]
            ),
            "sql_snippets": {
                "filters": sorted([build_filter(f) for f in filters], key=lambda x: x["id"]),
                "measures": sorted([build_measure(m) for m in measures], key=lambda x: x["id"]),
                "expressions": [],
            },
        },
        "benchmarks": {
            "questions": sorted(
                [build_benchmark(b) for b in benchmarks], key=lambda x: x["id"]
            )
        },
    }

    payload = {
        "title": room_config.get("title", room_config.get("room_name")),
        "description": room_config.get("description", ""),
        "warehouse_id": env["warehouse_id"],
        "parent_path": env.get("parent_path", room_config.get("parent_path", "")),
        "serialized_space": json.dumps(serialized_space),
    }
    return payload, serialized_space


def deploy(host, token, space_id, payload, dry_run=False):
    if dry_run:
        print("  [DRY RUN] Would deploy payload:")
        ss = json.loads(payload["serialized_space"])
        print(f"    example_sql count: {len(ss['instructions']['example_question_sqls'])}")
        print(f"    filter count: {len(ss['instructions']['sql_snippets']['filters'])}")
        print(f"    measure count: {len(ss['instructions']['sql_snippets']['measures'])}")
        print(f"    benchmark count: {len(ss['benchmarks']['questions'])}")
        return None

    if requests is None:
        raise ImportError("requests library required. Install: pip install requests")

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    if space_id:
        url = f"{host}/api/2.0/genie/spaces/{space_id}"
        response = requests.patch(url, headers=headers, json=payload, timeout=60)
    else:
        url = f"{host}/api/2.0/genie/spaces"
        response = requests.post(url, headers=headers, json=payload, timeout=60)

    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser(description="Push deployment kit folder to Genie room")
    parser.add_argument("--env", default="local", help="Environment name (default: local)")
    parser.add_argument("--dry-run", action="store_true", help="Assemble payload but do not deploy")
    args = parser.parse_args()

    print("Step 1: Validate...")
    errors = validate()
    if errors:
        for err in errors:
            print(f"  ERROR: {err}")
        print("Validation failed. Fix errors before deploying.")
        return 1
    print("  Validation passed.")

    print("Step 2: Load environment...")
    env = load_env(args.env)
    space_id = env.get("space_id")
    print(f"  Environment: {env.get('environment', args.env)}")
    print(f"  Workspace: {env.get('workspace_url', '(unknown)')}")
    print(f"  Space ID: {space_id or '(new room)'}")

    print("Step 3: Assemble payload...")
    payload, ss = assemble_payload(env)
    example_sql_count = len(ss["instructions"]["example_question_sqls"])
    filter_count = len(ss["instructions"]["sql_snippets"]["filters"])
    measure_count = len(ss["instructions"]["sql_snippets"]["measures"])
    bench_count = len(ss["benchmarks"]["questions"])
    print(f"  example_sql: {example_sql_count}")
    print(f"  filters: {filter_count}")
    print(f"  measures: {measure_count}")
    print(f"  benchmarks: {bench_count}")

    print("Step 4: Deploy...")
    host, token = get_auth()
    result = deploy(host, token, space_id, payload, args.dry_run)
    if result:
        new_space_id = result.get("space_id") or result.get("id")
        if new_space_id and not space_id:
            print(f"  New room created. Space ID: {new_space_id}")
            print(f"  Update env/{args.env}.yml with: space_id: {new_space_id}")
        print("  Deploy successful.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
