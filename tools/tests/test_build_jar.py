import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

from build_jar import build_jar  # noqa: E402


class BuildJarTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def test_jar_contains_only_pack_files(self):
        jar = build_jar(REPO_ROOT, Path(self.tmp))
        names = set(zipfile.ZipFile(jar).namelist())
        self.assertEqual(jar.name, "royaume-loutre-mer-datapack-0.1.0.jar")
        self.assertIn("fabric.mod.json", names)
        self.assertIn("pack.mcmeta", names)
        self.assertIn("data/cobblemon/starters/default.json", names)
        self.assertFalse([n for n in names if n.startswith(("tools/", "docs/", ".git", ".idea", "build/"))])
        self.assertFalse([n for n in names if "\\" in n])


if __name__ == "__main__":
    unittest.main()
