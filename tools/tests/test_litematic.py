import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

from litematic import load_litematic, trim  # noqa: E402
from nbtio import Double, Int, LongArray, write_nbt_file  # noqa: E402

SRC = REPO_ROOT / "tools/source/base.litematic"


def pack_states(ids, bits):
    """Encode des indices de palette comme Litematica (sans alignement)."""
    total = len(ids) * bits
    longs = [0] * (-(-total // 64))
    for i, v in enumerate(ids):
        start = i * bits
        li, off = divmod(start, 64)
        longs[li] |= (v << off) & 0xFFFFFFFFFFFFFFFF
        if off + bits > 64:
            longs[li + 1] |= v >> (64 - off)
    return LongArray(longs)


def region(size, position, palette, ids, tile_entities=(), entities=()):
    bits = max(2, (len(palette) - 1).bit_length())
    return {
        "Position": {"x": Int(position[0]), "y": Int(position[1]), "z": Int(position[2])},
        "Size": {"x": Int(size[0]), "y": Int(size[1]), "z": Int(size[2])},
        "BlockStatePalette": [{"Name": n} for n in palette],
        "BlockStates": pack_states(ids, bits),
        "TileEntities": list(tile_entities),
        "Entities": list(entities),
        "PendingBlockTicks": [], "PendingFluidTicks": [],
    }


def litematic(regions):
    return {"Version": Int(7), "MinecraftDataVersion": Int(3955),
            "Metadata": {"Name": "t"}, "Regions": regions}


class LitematicTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_loads_test_base(self):
        b = load_litematic(SRC)
        self.assertEqual(b.size, (82, 87, 81))
        self.assertEqual(b.data_version, 4438)
        self.assertEqual(sum(1 for i in b.blocks if b.palette[i]["Name"] != "minecraft:air"), 27660)
        self.assertEqual(b.block_name(41, 0, 40), "minecraft:oak_planks")
        self.assertEqual(b.block_name(41, 28, 40), "minecraft:glass")

    def test_trim_drops_empty_top_layers(self):
        t = trim(load_litematic(SRC))
        self.assertEqual(t.size, (82, 60, 81))
        self.assertEqual(t.block_name(41, 0, 40), "minecraft:oak_planks")
        self.assertEqual(t.block_name(41, 59, 40), "minecraft:glass")

    def test_negative_size_entities_and_block_entities(self):
        # 3 x 2 x 2, coffre au coin local (2, 0, 1), une entité
        sx, sy, sz = 3, 2, 2
        ids = [0] * (sx * sy * sz)
        ids[(0 * sz + 1) * sx + 2] = 1
        chest = {"x": Int(2), "y": Int(0), "z": Int(1), "id": "minecraft:chest", "Items": []}
        ent = {"id": "minecraft:armor_stand",
               "Pos": [Double(-1.5), Double(0.0), Double(0.5)]}
        path = self.tmp / "neg.litematic"
        write_nbt_file(path, litematic({"r": region((-3, 2, 2), (10, 5, 5),
                                                    ["minecraft:air", "minecraft:chest"], ids,
                                                    [chest], [ent])}))
        b = load_litematic(path)
        self.assertEqual(b.size, (3, 2, 2))
        self.assertEqual(b.block_name(2, 0, 1), "minecraft:chest")
        self.assertIn((2, 0, 1), b.block_entities)
        self.assertNotIn("x", b.block_entities[(2, 0, 1)])
        self.assertEqual(b.block_entities[(2, 0, 1)]["id"], "minecraft:chest")
        self.assertEqual(b.entities[0][0], (0.5, 0.0, 0.5))

    def test_trim_shifts_block_entities_and_entities(self):
        # 4 x 3 x 4 : seul bloc non-air en (2, 1, 3), avec entité de bloc et entité à côté
        sx, sy, sz = 4, 3, 4
        ids = [0] * (sx * sy * sz)
        ids[(1 * sz + 3) * sx + 2] = 1
        chest = {"x": Int(2), "y": Int(1), "z": Int(3), "id": "minecraft:chest"}
        inside = {"id": "minecraft:armor_stand", "Pos": [Double(2.5), Double(1.0), Double(3.5)]}
        outside = {"id": "minecraft:armor_stand", "Pos": [Double(0.5), Double(0.0), Double(0.5)]}
        path = self.tmp / "trim.litematic"
        write_nbt_file(path, litematic({"r": region((4, 3, 4), (0, 0, 0),
                                                    ["minecraft:air", "minecraft:chest"], ids,
                                                    [chest], [inside, outside])}))
        t = trim(load_litematic(path))
        self.assertEqual(t.size, (1, 1, 1))
        self.assertEqual(t.block_name(0, 0, 0), "minecraft:chest")
        self.assertEqual(list(t.block_entities), [(0, 0, 0)])
        self.assertEqual([p for p, _ in t.entities], [(0.5, 0.0, 0.5)])

    def test_rejects_multi_region(self):
        r = region((1, 1, 1), (0, 0, 0), ["minecraft:air", "minecraft:stone"], [1])
        path = self.tmp / "two.litematic"
        write_nbt_file(path, litematic({"a": r, "b": r}))
        with self.assertRaisesRegex(ValueError, "1 région"):
            load_litematic(path)


if __name__ == "__main__":
    unittest.main()
