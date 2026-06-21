#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MakefileRootTests(unittest.TestCase):
    def run_make(self, *arguments, environment=None, prefix="Orb's [gate] "):
        with tempfile.TemporaryDirectory(prefix=prefix) as directory:
            checkout = Path(directory)
            makefile = checkout / "Makefile"
            makefile.write_text(
                (ROOT / "Makefile").read_text(encoding="utf-8"), encoding="utf-8"
            )
            env = {"PATH": os.environ.get("PATH", "")}
            if environment:
                env.update(environment)
            return subprocess.run(
                ["make", "--no-print-directory", "-n", "-f", str(makefile), *arguments],
                cwd=checkout.parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
                env=env,
            )

    def run_live_make(self, target, prefix):
        with tempfile.TemporaryDirectory() as parent_directory:
            parent = Path(parent_directory)
            checkout = parent / prefix
            checkout.mkdir()
            shutil.copy2(ROOT / "Makefile", checkout / "Makefile")
            (checkout / "scripts").mkdir()
            (checkout / "tests").mkdir()
            (checkout / "scripts/check-baseline.py").touch()
            (checkout / "tests/test_workflow_contract.py").touch()
            (checkout / "tests/test_makefile_root.py").touch()

            bin_directory = parent / "bin"
            bin_directory.mkdir()
            log = parent / "commands.log"
            sentinel = parent / "command-substitution-ran"
            for command in ("go", "python3"):
                executable = bin_directory / command
                executable.write_text(
                    "#!/bin/sh\nprintf '%s\\t%s\\n' \"$PWD\" \"$*\" >> \"$COMMAND_LOG\"\n",
                    encoding="utf-8",
                )
                executable.chmod(0o755)
            attacker = bin_directory / "root_attack"
            attacker.write_text(
                "#!/bin/sh\n: > \"$ATTACK_SENTINEL\"\n",
                encoding="utf-8",
            )
            attacker.chmod(0o755)
            env = {
                "ATTACK_SENTINEL": str(sentinel),
                "COMMAND_LOG": str(log),
                "PATH": f"{bin_directory}:{os.environ.get('PATH', '')}",
            }
            result = subprocess.run(
                ["make", "--no-print-directory", "-f", str(checkout / "Makefile"), target],
                cwd=parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
                env=env,
            )
            command_log = log.read_text(encoding="utf-8") if log.exists() else ""
            return result, checkout, command_log, sentinel.exists()

    def test_all_targets_preserve_spaced_absolute_makefile_path(self):
        targets = (
            "build",
            "check",
            "lint",
            "race",
            "root-test",
            "static-check",
            "test",
            "verify",
            "vet",
            "workflow-contract",
        )
        for target in targets:
            for name, arguments, environment in (
                ("none", (target,), None),
                ("command", (target, "REPO_ROOT=/tmp/attacker-root"), None),
                ("environment", (target,), {"REPO_ROOT": "/tmp/attacker-root"}),
            ):
                with self.subTest(target=target, override=name):
                    result = self.run_make(*arguments, environment=environment)
                    self.assertEqual(result.returncode, 0, result.stdout)
                    self.assertNotIn("/tmp/attacker-root", result.stdout)
                    self.assertIn("$REPO_ROOT", result.stdout)

    def test_command_line_makefile_list_override_fails_closed(self):
        result = self.run_make("verify", "MAKEFILE_LIST=/tmp/untrusted")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MAKEFILE_LIST must not be overridden", result.stdout)

    def test_environment_makefile_list_override_fails_closed(self):
        result = self.run_make(
            "-e", "verify", environment={"MAKEFILE_LIST": "/tmp/untrusted"}
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MAKEFILE_LIST must not be overridden", result.stdout)

    def test_root_overrides_do_not_redirect_targets(self):
        for variable in ("ROOT", "REPO_ROOT"):
            for name, arguments, environment in (
                ("command", ("verify", f"{variable}=/tmp/attacker-root"), None),
                ("environment", ("verify",), {variable: "/tmp/attacker-root"}),
            ):
                with self.subTest(variable=variable, override=name):
                    result = self.run_make(*arguments, environment=environment)
                    self.assertEqual(result.returncode, 0, result.stdout)
                    self.assertNotIn("/tmp/attacker-root", result.stdout)

    def test_live_recipes_treat_hostile_checkout_path_as_data(self):
        hostile_path = " Orb's [gate] `root_attack` "
        targets = (
            "build", "check", "lint", "race", "root-test", "static-check",
            "test", "verify", "vet", "workflow-contract",
        )
        for target in targets:
            with self.subTest(target=target):
                result, checkout, log, attacked = self.run_live_make(target, hostile_path)
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertFalse(attacked, result.stdout)
                self.assertIn(str(checkout), log)


if __name__ == "__main__":
    unittest.main()
