"""Regression checks for synchronization and scan boundaries using synthetic fixtures."""
import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

RULES = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sync_skills", RULES / "sync-skills.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / ".claude/skills/example/SKILL.md"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("---\nname: example\ndescription: Example task.\n---\n# Example\n", encoding="utf-8")
        self.target = self.root / ".agents/skills/example/SKILL.md"

    def test_roundtrip_and_source_update(self):
        self.assertEqual(sync.synchronize(self.root)[0], 1)
        self.assertFalse(self.target.exists())
        self.assertEqual(sync.synchronize(self.root, write=True)[0], 0)
        self.assertEqual(sync.synchronize(self.root)[0], 0)
        self.source.write_bytes(self.source.read_bytes() + b"More context.\n")
        self.assertEqual(sync.synchronize(self.root, write=True)[0], 0)
        self.assertEqual(self.source.read_bytes(), self.target.read_bytes())

    def test_local_edit_is_preserved_even_with_adopt_after_initialization(self):
        sync.synchronize(self.root, write=True)
        self.target.write_bytes(b"user edit")
        self.assertEqual(sync.synchronize(self.root, write=True, adopt=True)[0], 1)
        self.assertEqual(self.target.read_bytes(), b"user edit")

    def test_initial_conflict_requires_explicit_adoption(self):
        self.target.parent.mkdir(parents=True)
        self.target.write_bytes(b"old copy")
        self.assertEqual(sync.synchronize(self.root, write=True)[0], 1)
        self.assertEqual(sync.synchronize(self.root, write=True, adopt=True)[0], 0)

    def test_missing_reference_prevents_all_writes(self):
        self.source.write_bytes(self.source.read_bytes() + b"Read `references/missing.md`.\n")
        self.assertEqual(sync.synchronize(self.root, write=True)[0], 1)
        self.assertFalse(self.target.exists())

    def test_extra_file_is_not_deleted(self):
        sync.synchronize(self.root, write=True)
        extra = self.target.parent / "notes.txt"
        extra.write_text("keep me", encoding="utf-8")
        self.assertEqual(sync.synchronize(self.root, write=True)[0], 1)
        self.assertEqual(extra.read_text(), "keep me")

    def test_linked_resource_is_rejected(self):
        outside = self.root / "outside.txt"
        outside.write_text("private", encoding="utf-8")
        try:
            (self.source.parent / "linked.txt").symlink_to(outside)
        except OSError:
            self.skipTest("OS does not permit symlinks")
        with self.assertRaises(ValueError):
            sync.synchronize(self.root, write=True)


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.bash = shutil.which("bash")
        if not self.bash and Path("C:/Program Files/Git/bin/bash.exe").exists():
            self.bash = "C:/Program Files/Git/bin/bash.exe"
        if not self.bash:
            self.skipTest("Bash unavailable")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        scripts = self.root / "docs/rules"
        scripts.mkdir(parents=True)
        for name in ("trace.sh", "msg.sh"):
            shutil.copyfile(RULES / name, scripts / name)
        for folder in ("client/src/legacy", "cell-app/src/main/java/master_data"):
            directory = self.root / folder
            directory.mkdir(parents=True)
            (directory / "secret.ts").write_text("R-DEMO-001\nconst CODE = \"MSG_PMKT-E-00001_001\";\n", encoding="utf-8")
        spec_dir = self.root / "docs/doing/demo-spec"
        spec_dir.mkdir(parents=True)
        (spec_dir / "02-rules.md").write_text("| R-DEMO-001 | Demo | FE BE | P1 | READY | fixture |\n", encoding="utf-8")
        pyc = self.root / "fixture-pyc"
        pyc.mkdir()
        (pyc / "6.messages.md").write_text("| MSG_PMKT-E-00001_001 | Fixture message |\n", encoding="utf-8")

    def run_script(self, command):
        return subprocess.run([self.bash, "-lc", command], cwd=self.root, capture_output=True, text=True, encoding="utf-8")

    def test_trace_grep_fallback_excludes_frozen_trees(self):
        for layer in ("be", "fe"):
            # Force only command -v rg to report unavailable, exercising the grep branch.
            result = self.run_script('command() { if [ "$1" = -v ] && [ "$2" = rg ]; then return 1; fi; builtin command "$@"; }; source docs/rules/trace.sh docs/doing/demo-spec ' + layer)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("MISSING 1", result.stdout)
            self.assertNotIn("secret.ts", result.stdout)

    def test_message_scan_excludes_frozen_trees(self):
        for layer in ("be", "fe"):
            result = self.run_script("bash docs/rules/msg.sh fixture-pyc " + layer)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("THIEU 1", result.stdout)
            self.assertNotIn("secret.ts", result.stdout)

    def test_phase2_input_rejected_before_read(self):
        for script in ("trace.sh", "msg.sh"):
            result = self.run_script("bash docs/rules/" + script + " Phase_2/nonexistent fe")
            self.assertEqual(result.returncode, 2, result.stderr)

    def test_allowed_source_is_still_scanned(self):
        active = self.root / "client/src/active.ts"
        active.write_text('R-DEMO-001\nconst CODE = "MSG_PMKT-E-00001_001";\n', encoding="utf-8")
        result = self.run_script("bash docs/rules/trace.sh docs/doing/demo-spec fe")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("NO-TEST 1", result.stdout)
        result = self.run_script("bash docs/rules/msg.sh fixture-pyc fe")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK 1", result.stdout)


if __name__ == "__main__":
    unittest.main()
