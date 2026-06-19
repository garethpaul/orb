#!/usr/bin/env python3
"""Regression tests for the temporary three-lane GitHub Actions bridge."""

from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/check.yml"
CHECKER = ROOT / "scripts/check-baseline.py"
EXPECTED_MATRIX = 'go-version: ["1.20.14", "1.25.3", "1.25.11"]'


class ThreeLaneWorkflowContractTest(unittest.TestCase):
    def test_workflow_has_exactly_three_real_test_lanes(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn(EXPECTED_MATRIX, workflow)
        self.assertNotIn("1.24.0", workflow)
        self.assertEqual(1, len(re.findall(r"(?m)^  test:\s*$", workflow)))
        self.assertEqual(1, len(re.findall(r"(?m)^      - run: make check\s*$", workflow)))
        self.assertIn("go-version: ${{ matrix.go-version }}", workflow)
        self.assertNotIn("continue-on-error:", workflow)
        self.assertNotIn("needs:", workflow)
        self.assertNotIn("if: always()", workflow)

    def test_checker_rejects_hostile_workflow_mutations(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(EXPECTED_MATRIX, workflow)
        mutations = {
            "drops protected lane": workflow.replace(
                EXPECTED_MATRIX,
                'go-version: ["1.20.14", "1.25.11"]',
            ),
            "introduces unsupported Go 1.24 lane": workflow.replace(
                "1.20.14", "1.24.0"
            ),
            "uses fake protected-context aggregator": workflow.replace(
                EXPECTED_MATRIX,
                'go-version: ["1.20.14", "1.25.11"]',
            )
            + "\n  compatibility:\n"
            + "    name: test (1.25.3)\n"
            + "    needs: test\n"
            + "    runs-on: ubuntu-24.04\n"
            + "    if: always()\n"
            + "    steps:\n"
            + "      - run: exit 0\n",
            "launders command with echo": workflow.replace(
                "- run: make check",
                "- run: echo make check",
            ),
            "runs only unit tests": workflow.replace(
                "- run: make check",
                "- run: go test ./...",
            ),
            "allows lane failure": workflow.replace(
                "    env:\n",
                "    continue-on-error: true\n    env:\n",
            ),
            "hard-codes setup toolchain": workflow.replace(
                "go-version: ${{ matrix.go-version }}",
                "go-version: 1.25.11",
            ),
            "renames emitted contexts": workflow.replace(
                "  test:\n",
                "  test:\n    name: aggregate\n",
            ),
            "adds an undeclared matrix lane": workflow.replace(
                "      matrix:\n",
                "      matrix:\n        include:\n          - go-version: 1.26.1\n",
            ),
        }

        self.assertTrue(all(content != workflow for content in mutations.values()))

        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory) / "orb"
            shutil.copytree(ROOT, repository, ignore=shutil.ignore_patterns(".git"))
            candidate_workflow = repository / ".github/workflows/check.yml"

            for name, mutated_workflow in mutations.items():
                with self.subTest(name=name):
                    candidate_workflow.write_text(mutated_workflow, encoding="utf-8")
                    result = subprocess.run(
                        ["python3", str(repository / CHECKER.relative_to(ROOT))],
                        cwd=repository,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertNotEqual(
                        0,
                        result.returncode,
                        f"checker accepted hostile mutation: {name}",
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
