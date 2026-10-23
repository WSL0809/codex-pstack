import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("port", Path(__file__).resolve().parents[1] / "scripts/port_upstream.py")
port = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(port)


class FrontmatterTests(unittest.TestCase):
    def test_folded_description_survives_host_metadata_conversion(self):
        original = b'---\nname: example\ndescription: >-\n  Build a useful tool.\n  Use it for this task.\ndisable-model-invocation: true\n---\n\n# Example\nOriginal procedure.\n'
        result = port.render("skills/example/SKILL.md", original).decode()
        self.assertIn("description: >-\n  Build a useful tool.\n  Use it for this task.\n---", result)
        self.assertTrue(result.endswith("\n# Example\nOriginal procedure.\n"))
        self.assertNotIn("disable-model-invocation:", result)


if __name__ == "__main__":
    unittest.main()
