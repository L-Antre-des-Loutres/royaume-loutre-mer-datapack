import contextlib
import io
import re
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
               "spawn": [41, 1, 40], "spawn_yaw": 0, "foundation_depth": 24}
FILL_RE = r"fill ~(-?\d+) ~(-?\d+) ~(-?\d+) ~(-?\d+) ~(-?\d+) ~(-?\d+) "


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
        half = (gen / "place_clockwise_180.mcfunction").read_text(encoding="utf-8")
        # argument de rotation des commandes 1.21.1 : none, clockwise_90, 180, counterclockwise_90
        self.assertIn("place template rlm_spawn:base/p_1_0_1 ~-41 ~0 ~-41 180", half)
        self.assertNotIn(" clockwise_180", half)
        self.assertIn("spawn.yaw set value -90",
                      (gen / "place_counterclockwise_90.mcfunction").read_text(encoding="utf-8"))
        # zone à charger : emprise du build (82 x 81) élargie des fondations (24 - 1)
        self.assertFalse((gen / "constants.mcfunction").exists())
        self.assertIn("forceload add ~-23 ~-23 ~104 ~103", (gen / "forceload_none.mcfunction").read_text(encoding="utf-8"))
        self.assertIn("forceload remove ~-23 ~-23 ~104 ~103", (gen / "unforceload_none.mcfunction").read_text(encoding="utf-8"))
        self.assertIn("forceload add ~-103 ~-23 ~23 ~104",
                      (gen / "forceload_clockwise_90.mcfunction").read_text(encoding="utf-8"))
        area = (gen / "area_loaded_none.mcfunction").read_text(encoding="utf-8")
        self.assertEqual(area.count("unless loaded"), 81)
        self.assertIn("execute unless loaded ~-23 ~ ~-23 run return fail", area)
        self.assertIn("execute unless loaded ~104 ~ ~103 run return fail", area)
        verify = (gen / "verify_none.mcfunction").read_text(encoding="utf-8")
        self.assertEqual(verify.count("run return fail"), 24 + 4)   # échantillon + 4 coins des fondations
        self.assertTrue(verify.rstrip().endswith("return 1"))
        self.assertEqual(len(list(gen.glob("*.mcfunction"))), 20)

    def test_foundation_is_filled_before_the_build(self):
        with contextlib.redirect_stderr(io.StringIO()):
            convert(BASE_CONFIG, self.out())
        gen = self.out() / "data/rlm_spawn/function/generated"
        place = (gen / "place_none.mcfunction").read_text(encoding="utf-8")
        filler = " minecraft:grass_block replace #minecraft:replaceable"
        self.assertIn("fill ~0 ~-1 ~0 ~81 ~-1 ~80" + filler, place)
        self.assertIn("fill ~-23 ~-24 ~-23 ~104 ~-24 ~103" + filler, place)
        self.assertEqual(place.count("\nfill "), 24)
        self.assertLess(place.index("\nfill "), place.index("place template"))
        cw = (gen / "place_clockwise_90.mcfunction").read_text(encoding="utf-8")
        self.assertIn("fill ~-80 ~-1 ~0 ~0 ~-1 ~81" + filler, cw)
        verify = (gen / "verify_none.mcfunction").read_text(encoding="utf-8")
        self.assertIn("execute if block ~0 ~-1 ~0 #minecraft:replaceable run return fail", verify)
        self.assertIn("execute if block ~81 ~-1 ~80 #minecraft:replaceable run return fail", verify)
        self.assertIn("execute if block ~-80 ~-1 ~81 #minecraft:replaceable run return fail",
                      (gen / "verify_clockwise_90.mcfunction").read_text(encoding="utf-8"))

    def test_no_foundation_by_default(self):
        src = self.synthetic((2, 1, 1), ["minecraft:air", "minecraft:stone"], [1, 1])
        convert({"litematic": src, "ground_layer": 0, "spawn": [0, 1, 0], "spawn_yaw": 0}, self.out())
        place = (self.out() / "data/rlm_spawn/function/generated/place_none.mcfunction").read_text(encoding="utf-8")
        self.assertNotIn("fill ", place)

    def test_fill_commands_stay_under_the_volume_limit(self):
        src = self.synthetic((200, 1, 1), ["minecraft:air", "minecraft:stone"], [1] * 200)
        convert({"litematic": src, "ground_layer": 0, "spawn": [0, 1, 0], "spawn_yaw": 0,
                 "foundation_depth": 20}, self.out())
        place = (self.out() / "data/rlm_spawn/function/generated/place_none.mcfunction").read_text(encoding="utf-8")
        fills = re.findall(FILL_RE, place)
        self.assertTrue(fills)
        covered = 0
        for x1, y1, z1, x2, y2, z2 in fills:
            vol = (abs(int(x2) - int(x1)) + 1) * (abs(int(y2) - int(y1)) + 1) * (abs(int(z2) - int(z1)) + 1)
            self.assertLessEqual(vol, 32768)
            if int(y1) == -20:
                covered += vol
        self.assertEqual(covered, (200 + 2 * 19) * (1 + 2 * 19))

    def test_ground_layer_minus_one_sits_on_the_surface(self):
        # -1 : le build est posé juste au-dessus de la surface (eau ou sol) sans la remplacer
        sx, sy, sz = 2, 3, 1
        ids = [1, 1, 0, 0, 0, 0]
        src = self.synthetic((sx, sy, sz), ["minecraft:air", "minecraft:stone"], ids)
        convert({"litematic": src, "ground_layer": -1, "spawn": [0, 1, 0], "spawn_yaw": 0}, self.out())
        # trim garde seulement la couche 0 (pierre) : 2 x 1 x 1
        gen = self.out() / "data/rlm_spawn/function/generated"
        place = (gen / "place_none.mcfunction").read_text(encoding="utf-8")
        self.assertIn("place template rlm_spawn:base/p_0_0_0 ~0 ~1 ~0 none", place)
        self.assertIn("execute positioned ~0 ~2 ~0 run function rlm_spawn:step/set_spawn", place)
        self.assertIn("execute unless block ~0 ~1 ~0 minecraft:stone", (gen / "verify_none.mcfunction").read_text(encoding="utf-8"))
        lot = read_nbt_file(self.out() / "data/rlm_spawn/structure/lot.nbt")
        self.assertEqual(list(lot["size"]), [2, 2, 1])

    def test_rejects_ground_layer_below_minus_one(self):
        src = self.synthetic((2, 1, 1), ["minecraft:air", "minecraft:stone"], [1, 1])
        with self.assertRaises(ValueError):
            convert({"litematic": src, "ground_layer": -2, "spawn": [0, 1, 0], "spawn_yaw": 0}, self.out())

    def test_old_build_keeps_its_data_version_for_the_game_upgrade(self):
        # build 1.16.5 : le jeu met à jour les blocs et panneaux au chargement si on garde la version
        src = self.synthetic((2, 1, 1), ["minecraft:air", "minecraft:stone", "minecraft:grass"], [1, 2],
                             data_version=2586)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            convert({"litematic": src, "ground_layer": 0, "spawn": [0, 1, 0], "spawn_yaw": 0}, self.out())
        piece = read_nbt_file(self.out() / "data/rlm_spawn/structure/base/p_0_0_0.nbt")
        self.assertEqual(piece["DataVersion"], 2586)
        self.assertEqual([p["Name"] for p in piece["palette"]], ["minecraft:stone", "minecraft:grass"])
        verify = (self.out() / "data/rlm_spawn/function/generated/verify_none.mcfunction").read_text(encoding="utf-8")
        self.assertIn("minecraft:short_grass", verify)     # nom après mise à jour par le jeu
        self.assertNotIn("minecraft:grass ", verify)
        self.assertEqual(err.getvalue(), "")

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
        src = self.synthetic((250, 1, 250), ["minecraft:air", "minecraft:stone"], [1] * (250 * 250))
        with self.assertRaisesRegex(ValueError, "256"):
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
