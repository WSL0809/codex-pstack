import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/poteto-mode/scripts/worktree-audit.sh"


@unittest.skipUnless(shutil.which("git") and shutil.which("bash"), "requires git and bash")
class WorktreeAdapterTests(unittest.TestCase):
    def test_missing_history_does_not_mark_a_merged_worktree_safe(self):
        with tempfile.TemporaryDirectory(prefix="pstack-audit-") as temporary:
            root = Path(temporary)
            repo = root / "repo"
            repo.mkdir()
            def git(*args):
                subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)
            git("init", "-b", "main")
            git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-m", "fixture")
            git("worktree", "add", "-b", "candidate", str(root / "candidate"))
            bin_dir = root / "bin"
            bin_dir.mkdir()
            for name in ("gh", "origin"):
                stub = bin_dir / name
                stub.write_text("#!/bin/sh\nexit 1\n")
                stub.chmod(0o755)
            env = dict(os.environ)
            env.pop("PSTACK_TRANSCRIPTS_DIR", None)
            env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
            result = subprocess.run(["bash", str(SCRIPT), "-b", "main", str(repo)], env=env, capture_output=True, text=True, check=True, timeout=15)
            self.assertIn("review-no-history", result.stdout)
            self.assertNotIn("\tsafe\t", result.stdout)
            self.assertIn("activity is unknown", result.stderr)


if __name__ == "__main__":
    unittest.main()
