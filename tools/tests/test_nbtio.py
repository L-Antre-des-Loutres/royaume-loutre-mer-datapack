import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

from nbtio import (Byte, ByteArray, Double, Float, Int, IntArray, Long,  # noqa: E402
                   LongArray, Short, read_nbt_file, write_nbt_file)


class NbtIoTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "t.nbt"

    def tearDown(self):
        self._tmp.cleanup()

    def test_round_trip_keeps_types(self):
        root = {"b": Byte(-3), "s": Short(7), "i": Int(3955), "l": Long(2 ** 40), "f": Float(0.5),
                "d": Double(1.25), "t": "é", "list": [Int(1), Int(2)], "empty": [],
                "c": {"n": [Double(0.5)]}, "ba": ByteArray([1, -2]), "ia": IntArray([1, -2]),
                "la": LongArray([2 ** 64 - 1, 5])}
        write_nbt_file(self.path, root)
        back = read_nbt_file(self.path)
        self.assertEqual(back, root)
        for k in root:
            self.assertIs(type(back[k]), type(root[k]), k)
        self.assertIs(type(back["c"]["n"][0]), Double)

    def test_output_is_reproducible(self):
        root = {"i": Int(1)}
        write_nbt_file(self.path, root)
        first = self.path.read_bytes()
        import time
        time.sleep(1.1)
        write_nbt_file(self.path, root)
        self.assertEqual(self.path.read_bytes(), first)

    def test_reads_test_litematic(self):
        root = read_nbt_file(REPO_ROOT / "tools/source/base.litematic")
        self.assertEqual(root["MinecraftDataVersion"], 4438)
        self.assertEqual(root["Metadata"]["TotalBlocks"], 27660)


if __name__ == "__main__":
    unittest.main()
