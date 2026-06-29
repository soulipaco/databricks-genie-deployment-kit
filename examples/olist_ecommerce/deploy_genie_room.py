#!/usr/bin/env python3
"""
Deploy the Olist E-Commerce Genie room from this example folder.

Authentication:
  Set DATABRICKS_HOST and DATABRICKS_TOKEN in your shell.

Example:
  python examples/olist_ecommerce/deploy_genie_room.py --warehouse-id c3f37b7054223373

To update an existing room:
  python examples/olist_ecommerce/deploy_genie_room.py --warehouse-id c3f37b7054223373 --space-id <space_id>
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path

import requests
import yaml

EXAMPLE_ROOT = Path(__file__).resolve().parent


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_all_yaml(directory: Path):
    if not directory.exists():
        return []
    items = []
    for path in sorted(directory.glob("*.yml")):
        data = load_yaml(path)
        if data:
            items.append(data)
    return items


def build_sample_question(item: dict) -> dict:
    return {"id": item["id"], "question": [item["question"]]}


def build_example_sql(item: dict) -> dict:
    entry = {
        "id": item["id"],
        "question": [item["question"]],
        "sql": [item["sql"]],
    }
    if item.get("usage_guidance"):
        entry["usage_guidance"] = [item["usage_guidance"]]
    return entry


def build_filter(item: dict) -> dict:
    entry = {
        "id": item["id"],
        "display_name": item.get("display_name", ""),
        "sql": [item["sql"]],
    }
    if item.get("synonyms"):
        entry["synonyms"] = item["synonyms"]
    if item.get("instruction"):
        entry["instruction"] = [item["instruction"]]
    return entry


def build_measure(item: dict) -> dict:
    entry = {
        "id": item["id"],
        "alias": item.get("alias", ""),
        "display_name": item.get("display_name", ""),
        "sql": [item["sql"]],
    }
    if item.get("synonyms"):
        entry["synonyms"] = item["synonyms"]
    if item.get("instruction"):
        entry["instruction"] = [item["instruction"]]
    return entry


def build_benchmark(item: dict) -> dict:
    return {
        "id": item["id"],
        "question": [item["question"]],
        "answer": [{"format": item.get("answer_format", "SQL"), "content": [item.get("sql", "")]}],
    }


def assemble_payload(warehouse_id: str, parent_path: str) -> dict:
    room_config = load_yaml(EXAMPLE_ROOT / "room.config.yml")
    tables_config = load_yaml(EXAMPLE_ROOT / "data_sources" / "tables.yml")
    general_text = load_text(EXAMPLE_ROOT / "instructions" / "general.md")

    tables_payload = []
    for table in tables_config.get("tables") or []:
        col_configs = []
        col_meta_file = table.get("column_metadata_file")
        if col_meta_file:
            col_meta = load_yaml(EXAMPLE_ROOT / col_meta_file)
            for col in col_meta.get("columns") or []:
                col_entry = {"column_name": col["column_name"]}
                for flag in [
                    "exclude",
                    "enable_format_assistance",
                    "enable_entity_matching",
                ]:
                    if flag in col:
                        col_entry[flag] = col[flag]
                col_configs.append(col_entry)
            col_configs = sorted(col_configs, key=lambda x: x["column_name"])
        tables_payload.append(
            {
                "identifier": table["identifier"],
                "description": [table.get("description", "")],
                "column_configs": col_configs,
            }
        )

    example_sqls = load_all_yaml(EXAMPLE_ROOT / "instructions" / "example_sql")
    filters = load_all_yaml(EXAMPLE_ROOT / "instructions" / "sql_snippets" / "filters")
    measures = load_all_yaml(EXAMPLE_ROOT / "instructions" / "sql_snippets" / "measures")
    benchmarks = load_all_yaml(EXAMPLE_ROOT / "benchmarks")

    serialized_space = {
        "version": 2,
        "config": {
            "sample_questions": sorted(
                [build_sample_question(q) for q in room_config.get("sample_questions", [])],
                key=lambda x: x["id"],
            )
        },
        "data_sources": {"tables": sorted(tables_payload, key=lambda x: x["identifier"])},
        "instructions": {
            "text_instructions": [{"id": uuid.uuid4().hex, "content": [general_text]}],
            "example_question_sqls": sorted([build_example_sql(e) for e in example_sqls], key=lambda x: x["id"]),
            "sql_snippets": {
                "filters": sorted([build_filter(f) for f in filters], key=lambda x: x["id"]),
                "measures": sorted([build_measure(m) for m in measures], key=lambda x: x["id"]),
                "expressions": [],
            },
        },
        "benchmarks": {"questions": sorted([build_benchmark(b) for b in benchmarks], key=lambda x: x["id"])},
    }

    return {
        "title": room_config["title"],
        "description": room_config["description"],
        "warehouse_id": warehouse_id,
        "parent_path": parent_path,
        "serialized_space": json.dumps(serialized_space),
    }


def deploy(payload: dict, space_id: str | None, dry_run: bool = False) -> dict | None:
    host = os.environ.get("DATABRICKS_HOST", "").rstrip("/")
    token = os.environ.get("DATABRICKS_TOKEN")
    if not host or not token:
        raise RuntimeError("Set DATABRICKS_HOST and DATABRICKS_TOKEN before deploying.")

    if dry_run:
        serialized_space = json.loads(payload["serialized_space"])
        print("Dry run payload summary:")
        print(f"  title: {payload['title']}")
        print(f"  warehouse_id: {payload['warehouse_id']}")
        print(f"  parent_path: {payload['parent_path']}")
        print(f"  tables: {len(serialized_space['data_sources']['tables'])}")
        print(f"  sample questions: {len(serialized_space['config']['sample_questions'])}")
        print(f"  example SQL: {len(serialized_space['instructions']['example_question_sqls'])}")
        print(f"  filters: {len(serialized_space['instructions']['sql_snippets']['filters'])}")
        print(f"  measures: {len(serialized_space['instructions']['sql_snippets']['measures'])}")
        print(f"  benchmarks: {len(serialized_space['benchmarks']['questions'])}")
        return None

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    if space_id:
        url = f"{host}/api/2.0/genie/spaces/{space_id}"
        response = requests.patch(url, headers=headers, json=payload, timeout=60)
    else:
        url = f"{host}/api/2.0/genie/spaces"
        response = requests.post(url, headers=headers, json=payload, timeout=60)

    if response.status_code >= 400:
        raise RuntimeError(f"Genie API request failed ({response.status_code}): {response.text}")
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy Olist E-Commerce Genie room")
    parser.add_argument("--warehouse-id", required=True, help="Databricks SQL warehouse ID")
    parser.add_argument(
        "--parent-path",
        default=os.environ.get("DATABRICKS_PARENT_PATH", "/Users/<your-email>"),
        help="Workspace folder for the Genie room",
    )
    parser.add_argument("--space-id", default=None, help="Existing Genie space ID to update")
    parser.add_argument("--dry-run", action="store_true", help="Assemble payload without deploying")
    args = parser.parse_args()

    payload = assemble_payload(args.warehouse_id, args.parent_path)
    result = deploy(payload, args.space_id, args.dry_run)
    if result:
        new_space_id = result.get("space_id") or result.get("id")
        print("Deploy successful.")
        if new_space_id:
            print(f"Space ID: {new_space_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
