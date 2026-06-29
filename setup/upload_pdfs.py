#!/usr/bin/env python3
"""
upload_pdfs.py — Local helper to upload generated playbook PDFs to a UC Volume.

Run this from your local machine (or CI) BEFORE running setup/vector_search.py
when source_type is set to "volume" in pipeline_config.yml.

Usage:
    python setup/upload_pdfs.py [--config PATH] [--dry-run]

Requirements (install locally, not in Databricks):
    pip install databricks-sdk pyyaml

The script reads pipeline_config.yml, finds all source PDF files under
playbooks.local_path (relative to the repo root), and uploads them to
playbooks.volume_path using the Databricks Files API.

Authentication: uses your local ~/.databrickscfg or DATABRICKS_HOST /
DATABRICKS_TOKEN environment variables — the same credentials used by the CLI.
"""

import argparse
import os
import re
import sys
from pathlib import Path

import yaml


# ── Helpers ──────────────────────────────────────────────────────────────────

def _find_repo_root() -> Path:
    """Walk up from this file until we find pipeline_config.yml or git root."""
    here = Path(__file__).resolve().parent
    for candidate in [here, here.parent, here.parent.parent]:
        if (candidate / "pipeline" / "pipeline_config.yml").exists():
            return candidate
    raise FileNotFoundError(
        "Could not locate repo root (looked for pipeline/pipeline_config.yml). "
        "Run this script from within the deployment kit directory."
    )


def _find_placeholders(obj, path="") -> list:
    found = []
    if isinstance(obj, str):
        for match in re.finditer(r"\{\{[^}]+\}\}", obj):
            found.append((path, match.group(0)))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            found.extend(_find_placeholders(v, path=f"{path}.{k}" if path else k))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            found.extend(_find_placeholders(item, path=f"{path}[{i}]"))
    return found


def load_config(config_path: Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    placeholders = _find_placeholders(cfg)
    if placeholders:
        lines = "\n".join(f"  • {p}: {v}" for p, v in placeholders)
        raise ValueError(
            f"pipeline_config.yml contains unconfigured placeholder(s):\n{lines}\n\n"
            f"Fill in all {{{{PLACEHOLDER}}}} values before uploading."
        )
    return cfg


# ── Upload logic ──────────────────────────────────────────────────────────────

def upload_pdfs(cfg: dict, repo_root: Path, dry_run: bool = False) -> None:
    source_type = cfg["playbooks"]["source_type"]
    if source_type != "volume":
        print(
            f"source_type is '{source_type}' — no upload needed.\n"
            "Set source_type: volume in pipeline_config.yml to use UC Volumes."
        )
        return

    volume_path  = cfg["playbooks"]["volume_path"].rstrip("/")
    local_path   = cfg["playbooks"]["local_path"].lstrip("/")
    sources      = cfg["playbooks"].get("sources", [])

    if not volume_path:
        raise ValueError("playbooks.volume_path must be set when source_type is 'volume'.")
    if not sources:
        raise ValueError("playbooks.sources is empty — nothing to upload.")

    from databricks.sdk import WorkspaceClient
    w = WorkspaceClient()

    for source in sources:
        pdf_file     = source["pdf_file"]
        local_file   = repo_root / local_path / pdf_file
        remote_path  = f"{volume_path}/{pdf_file}"

        if not local_file.exists():
            print(f"  MISSING: {local_file}")
            print(f"  Run: python pipeline_playbook_generator/generate_playbook.py --kit-format genie_kit")
            print(f"  Then re-run this script.\n")
            continue

        size_kb = local_file.stat().st_size / 1024
        print(f"  {'[DRY-RUN] ' if dry_run else ''}Uploading {pdf_file} ({size_kb:.1f} KB)")
        print(f"    {local_file}")
        print(f"    → {remote_path}")

        if not dry_run:
            with open(local_file, "rb") as f:
                w.files.upload(remote_path, f, overwrite=True)
            print(f"    Done.")
        print()

    if not dry_run:
        print("Upload complete. Run setup/vector_search.py next to index the PDFs.")
    else:
        print("[DRY-RUN] No files were uploaded.")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--config", default=None,
        help="Path to pipeline_config.yml (default: auto-detected from repo root)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be uploaded without actually uploading.",
    )
    args = parser.parse_args()

    try:
        repo_root = _find_repo_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    config_path = Path(args.config) if args.config else repo_root / "pipeline" / "pipeline_config.yml"

    print(f"Repo root   : {repo_root}")
    print(f"Config file : {config_path}")
    print()

    try:
        cfg = load_config(config_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    upload_pdfs(cfg, repo_root, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
