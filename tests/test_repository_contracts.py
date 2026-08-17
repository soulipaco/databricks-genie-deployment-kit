import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


KIT_ROOT = Path(__file__).resolve().parents[1]
ASSET_PATHS = {
    "filters": ("instructions/sql_snippets/filters",),
    "measures": ("instructions/sql_snippets/measures",),
    "example_sql": ("instructions/example_sql",),
}


def load_yaml(path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


class ValidatorContractsTest(unittest.TestCase):
    def test_only_the_three_documented_template_warnings_remain(self):
        result = subprocess.run(
            [
                sys.executable,
                "scripts/validate.py",
                "--output",
                "json",
                "--fail-on-unexpected-warnings",
            ],
            cwd=KIT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(result.stdout)

        self.assertEqual("PASS", report["status"])
        self.assertEqual([], report["errors"])
        self.assertEqual([], report["unexpected_warnings"])
        self.assertEqual(
            [
                (
                    "TEMPLATE_COLUMN_METADATA_PLACEHOLDER",
                    "Column metadata file missing: metadata/columns/{{TABLE_1}}.yml",
                ),
                (
                    "TEMPLATE_ENV_PLACEHOLDER",
                    "local.yml: contains unfilled {{PLACEHOLDER}} values",
                ),
                (
                    "TEMPLATE_ENV_PLACEHOLDER",
                    "prod.yml: contains unfilled {{PLACEHOLDER}} values",
                ),
            ],
            [(item["code"], item["message"]) for item in report["warning_details"]],
        )


class MaterializationContractsTest(unittest.TestCase):
    def assert_activation_resolves_to_corpus(self, kit_root, require_deployed=False):
        library = kit_root / "instruction_library"
        for asset_type, output_parts in ASSET_PATHS.items():
            manifest = load_yaml(
                library / "activation" / f"{asset_type}.active.yml"
            )
            active_ids = manifest.get("active_ids") or []
            corpus_files = sorted((library / "corpus" / asset_type).glob("*.yml"))
            corpus_by_id = {load_yaml(path)["id"]: path for path in corpus_files}
            self.assertEqual(len(active_ids), len(set(active_ids)))
            for active_id in active_ids:
                self.assertIn(active_id, corpus_by_id)
            if require_deployed:
                output_dir = kit_root.joinpath(*output_parts)
                output_files = sorted(output_dir.glob("*.yml"))
                deployed_by_id = {
                    load_yaml(path)["id"]: path for path in output_files
                }
                self.assertEqual(set(active_ids), set(deployed_by_id))
                for active_id in active_ids:
                    self.assertEqual(
                        corpus_by_id[active_id].read_bytes(),
                        deployed_by_id[active_id].read_bytes(),
                    )

    def test_root_template_materialization_contract(self):
        self.assert_activation_resolves_to_corpus(KIT_ROOT, require_deployed=True)

    def test_sample_kit_materialization_contract(self):
        self.assert_activation_resolves_to_corpus(
            KIT_ROOT / "examples" / "sample_sales_analytics"
        )


if __name__ == "__main__":
    unittest.main()
