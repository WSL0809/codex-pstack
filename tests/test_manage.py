import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("manage", Path(__file__).resolve().parents[1] / "scripts/manage.py")
manage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manage)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source with spaces"
        self.target = self.root / "destination with spaces"
        (self.source / "skills/pstack/references").mkdir(parents=True)
        (self.source / "plugin.json").write_text('{"version":"0.1.0"}')
        (self.source / "skills/pstack/SKILL.md").write_text("first version")
        (self.source / "skills/pstack/references/check.md").write_text("evidence")

    def run_action(self, action):
        return manage.manage(action, self.target, self.source)

    def test_install_is_independent_and_repeatable(self):
        self.assertEqual(self.run_action("install")["action"], "installed")
        self.assertFalse((self.target / "pstack").is_symlink())
        self.assertEqual(self.run_action("install")["action"], "unchanged")
        self.assertEqual(self.run_action("status")["skills"], {"pstack": "ok"})
        (self.source / "skills/pstack/SKILL.md").write_text("changed source")
        self.assertEqual((self.target / "pstack/SKILL.md").read_text(), "first version")

    def test_update_and_remove_obsolete_file(self):
        self.run_action("install")
        (self.source / "skills/pstack/SKILL.md").write_text("second version")
        (self.source / "skills/pstack/references/check.md").unlink()
        self.assertEqual(self.run_action("update")["action"], "updated")
        self.assertEqual((self.target / "pstack/SKILL.md").read_text(), "second version")
        self.assertFalse((self.target / "pstack/references/check.md").exists())

    def test_uninstall_preserves_unrelated_skills(self):
        self.run_action("install")
        (self.target / "other").mkdir()
        (self.target / "other/SKILL.md").write_text("user data")
        self.run_action("uninstall")
        self.assertFalse((self.target / "pstack").exists())
        self.assertEqual((self.target / "other/SKILL.md").read_text(), "user data")
        self.assertEqual(self.run_action("uninstall")["action"], "not-installed")

    def test_collision_is_not_overwritten(self):
        (self.target / "pstack").mkdir(parents=True)
        (self.target / "pstack/SKILL.md").write_text("mine")
        with self.assertRaisesRegex(ValueError, "collision"):
            self.run_action("install")
        self.assertEqual((self.target / "pstack/SKILL.md").read_text(), "mine")
        self.assertFalse((self.target / manage.RECEIPT).exists())

    def test_edited_or_extra_files_block_update_and_uninstall(self):
        self.run_action("install")
        (self.target / "pstack/notes.txt").write_text("local work")
        for action in ("install", "update", "uninstall"):
            with self.assertRaisesRegex(ValueError, "Local changes"):
                self.run_action(action)
        self.assertEqual(self.run_action("status")["skills"]["pstack"], "modified")
        self.assertEqual((self.target / "pstack/notes.txt").read_text(), "local work")

    def test_missing_skill_can_be_repaired(self):
        self.run_action("install")
        manage.shutil.rmtree(self.target / "pstack")
        self.assertEqual(self.run_action("status")["skills"]["pstack"], "missing")
        self.run_action("update")
        self.assertEqual(self.run_action("status")["skills"]["pstack"], "ok")

    def test_symlink_collision_is_preserved(self):
        self.target.mkdir()
        (self.target / "pstack").symlink_to(self.source / "skills/pstack", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "collision"):
            self.run_action("install")
        self.assertTrue((self.target / "pstack").is_symlink())

    def test_receipt_path_traversal_is_rejected(self):
        self.target.mkdir()
        (self.target / manage.RECEIPT).write_text(json.dumps({"package": manage.PACKAGE_ID, "skills": {"../outside": {"SKILL.md": "0" * 64}}}))
        with self.assertRaisesRegex(ValueError, "Invalid skill"):
            self.run_action("uninstall")

    def test_live_lock_blocks_mutation(self):
        self.target.mkdir()
        (self.target / manage.LOCK).write_text("another installer")
        with self.assertRaisesRegex(ValueError, "lock exists"):
            self.run_action("install")
        self.assertEqual((self.target / manage.LOCK).read_text(), "another installer")

    def test_failed_update_restores_previous_installation(self):
        self.run_action("install")
        old_receipt = (self.target / manage.RECEIPT).read_bytes()
        (self.source / "skills/pstack/SKILL.md").write_text("next")
        with patch.object(manage.os, "replace", side_effect=OSError("disk full")):
            with self.assertRaisesRegex(OSError, "disk full"):
                self.run_action("update")
        self.assertEqual((self.target / "pstack/SKILL.md").read_text(), "first version")
        self.assertEqual((self.target / manage.RECEIPT).read_bytes(), old_receipt)
        self.assertFalse((self.target / manage.LOCK).exists())
        self.assertFalse(list(self.target.glob(".pstack-stage-*")))

    def test_source_symlink_is_rejected(self):
        (self.source / "skills/pstack/link").symlink_to(self.source / "plugin.json")
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.run_action("install")
        self.assertFalse((self.target / "pstack").exists())

    def test_status_does_not_create_target(self):
        self.assertFalse(self.run_action("status")["installed"])
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main()
