import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from convert_spawn_base import convert, rotate_offset, split_axis  # noqa: E402
from nbtio import Int, read_nbt_file, write_nbt_file  # noqa: E402
from test_litematic import litematic, region  # noqa: E402

BASE_CONFIG = {"litematic": "tools/source/base.litematic", "ground_layer": 0,
               "spawn": [41, 1, 40], "spawn_yaw": 0}


def written_positions(piece):
    return {tuple(int(c) for c in b["pos"]) for b in piece["blocks"]}


def non_air_count(piece):
    names = [p["Name"] for p in piece["palette"]]
    return sum(1 for b in piece["blocks"] if names[b["state"]] != "minecraft:air")


class ConvertTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def synthetic(self, size, palette, ids, data_version=3955, tile_entities=()):
        path = self.tmp / "synthetic.litematic"
        root = litematic({"r": region(size, (0, 0, 0), palette, ids, tile_entities)})
        root["MinecraftDataVersion"] = Int(data_version)
        write_nbt_file(path, root)
        return str(path)

    def out(self):
        return self.tmp / "out"

    def test_split_axis(self):
        self.assertEqual(split_axis(81), [(0, 41), (41, 40)])
        self.assertEqual(split_axis(48), [(0, 48)])
        self.assertEqual(split_axis(49), [(0, 25), (25, 24)])
        self.assertEqual(split_axis(100), [(0, 34), (34, 33), (67, 33)])

    def test_rotate_offset(self):
        self.assertEqual(rotate_offset(3, 5, "none"), (3, 5))
        self.assertEqual(rotate_offset(3, 5, "clockwise_90"), (-5, 3))
        self.assertEqual(rotate_offset(3, 5, "clockwise_180"), (-3, -5))
        self.assertEqual(rotate_offset(3, 5, "counterclockwise_90"), (5, -3))

    def test_converts_test_base(self):
        out = self.out()
        stale = out / "data/rlm_spawn/structure/base/old.nbt"
        stale.parent.mkdir(parents=True)
        stale.write_bytes(b"x")
        with contextlib.redirect_stderr(io.StringIO()):
            convert(BASE_CONFIG, out)
        base = out / "data/rlm_spawn/structure/base"
        names = sorted(p.stem for p in base.glob("*.nbt"))
        self.assertEqual(len(names), 8)
        self.assertNotIn("old", names)
        p = read_nbt_file(base / "p_1_0_1.nbt")
        self.assertEqual(list(p["size"]), [41, 30, 40])
        self.assertEqual(p["DataVersion"], 3955)
        self.assertEqual(sum(non_air_count(read_nbt_file(base / (n + ".nbt"))) for n in names), 27660)
        lot = read_nbt_file(out / "data/rlm_spawn/structure/lot.nbt")
        self.assertEqual(list(lot["size"]), [82, 60, 81])
        self.assertEqual(lot["entities"][0]["nbt"]["Tags"], ["rlm_spawn.anchor"])
        gen = out / "data/rlm_spawn/function/generated"
        place = (gen / "place_clockwise_90.mcfunction").read_text(encoding="utf-8")
        self.assertIn("place template rlm_spawn:base/p_1_0_1 ~-41 ~0 ~41 clockwise_90", place)
        self.assertIn("spawn.yaw set value 90", place)
        self.assertIn("execute positioned ~-40 ~1 ~41 run function rlm_spawn:step/set_spawn", place)
        self.assertIn("function rlm_spawn:generated/verify_clockwise_90", place)
        self.assertIn("spawn.yaw set value -90",
                      (gen / "place_counterclockwise_90.mcfunction").read_text(encoding="utf-8"))
        self.assertIn("#reach rlm_spawn 96", (gen / "constants.mcfunction").read_text(encoding="utf-8"))
        self.assertEqual((gen / "area_loaded.mcfunction").read_text(encoding="utf-8").count("unless loaded"), 169)
        verify = (gen / "verify_none.mcfunction").read_text(encoding="utf-8")
        self.assertEqual(verify.count("run return fail"), 24)
        self.assertTrue(verify.rstrip().endswith("return 1"))
        self.assertEqual(len(list(gen.glob("*.mcfunction"))), 10)

    def test_buried_exterior_air_is_omitted(self):
        # 5x3x5, ground_layer 2 : sol de pierre plein en y=0, anneau en y=1 autour de (2, 1, 2)
        sx, sy, sz = 5, 3, 5
        ids = [0] * (sx * sy * sz)

        def put(x, y, z):
            ids[(y * sz + z) * sx + x] = 1
        for x in range(1, 4):
            for z in range(1, 4):
                put(x, 0, z)
                if (x, z) != (2, 2):
                    put(x, 1, z)
        put(0, 2, 0)
        put(4, 2, 4)
        src = self.synthetic((5, 3, 5), ["minecraft:air", "minecraft:stone"], ids)
        convert({"litematic": src, "ground_layer": 2, "spawn": [1, 2, 1], "spawn_yaw": 0}, self.out())
        piece = read_nbt_file(self.out() / "data/rlm_spawn/structure/base/p_0_0_0.nbt")
        pos = written_positions(piece)
        self.assertIn((2, 1, 2), pos)       # air enfermé
        self.assertNotIn((0, 0, 0), pos)    # air extérieur enterré
        self.assertNotIn((0, 1, 4), pos)
        self.assertIn((2, 2, 2), pos)       # air au-dessus du sol
        self.assertEqual(list(read_nbt_file(self.out() / "data/rlm_spawn/structure/lot.nbt")["size"]), [5, 1, 5])

    def test_block_entity_lands_in_its_piece(self):
        ids = [1] * 50
        ids[30] = 2
        chest = {"x": Int(30), "y": Int(0), "z": Int(0), "id": "minecraft:chest", "Lock": "clé"}
        src = self.synthetic((50, 1, 1), ["minecraft:air", "minecraft:stone", "minecraft:chest"], ids,
                             tile_entities=[chest])
        convert({"litematic": src, "ground_layer": 0, "spawn": [0, 1, 0], "spawn_yaw": 0}, self.out())
        piece = read_nbt_file(self.out() / "data/rlm_spawn/structure/base/p_1_0_0.nbt")
        with_nbt = [b for b in piece["blocks"] if "nbt" in b]
        self.assertEqual(len(with_nbt), 1)
        self.assertEqual([int(c) for c in with_nbt[0]["pos"]], [5, 0, 0])
        self.assertEqual(with_nbt[0]["nbt"]["Lock"], "clé")
        self.assertNotIn("x", with_nbt[0]["nbt"])

    def test_rejects_oversized_build(self):
        src = self.synthetic((230, 1, 1), ["minecraft:air", "minecraft:stone"], [1] * 230)
        with self.assertRaisesRegex(ValueError, "224"):
            convert({"litematic": src, "ground_layer": 0, "spawn": [0, 1, 0], "spawn_yaw": 0}, self.out())
        self.assertFalse(self.out().exists())

    def test_rejects_spawn_inside_block(self):
        with self.assertRaises(ValueError):
            convert(dict(BASE_CONFIG, spawn=[41, 0, 40]), self.out())
        self.assertFalse(self.out().exists())

    def test_warns_on_foreign_blocks(self):
        src = self.synthetic((2, 1, 1), ["minecraft:air", "minecraft:stone", "chipped:x"], [1, 2],
                             data_version=4438)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            convert({"litematic": src, "ground_layer": 0, "spawn": [0, 1, 0], "spawn_yaw": 0}, self.out())
        self.assertIn("chipped:x", err.getvalue())
        self.assertIn("4438", err.getvalue())
        self.assertIn("minecraft:stone", err.getvalue())


if __name__ == "__main__":
    unittest.main()
