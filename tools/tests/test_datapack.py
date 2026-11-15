"""Cohérence statique du datapack : JSON valides, références existantes."""
import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data"


def resource_path(rid: str, folder: str, ext: str) -> Path:
    ns, _, path = rid.partition(":")
    return DATA / ns / folder / (path + ext)


class DatapackTest(unittest.TestCase):
    def test_all_json_parse(self):
        files = list(DATA.rglob("*.json"))
        self.assertTrue(files)
        for f in files:
            with self.subTest(f=str(f.relative_to(REPO_ROOT))):
                json.loads(f.read_text(encoding="utf-8"))

    def test_function_references_exist(self):
        refs = set()
        for f in DATA.rglob("*.mcfunction"):
            refs |= set(re.findall(r"function (rlm_spawn:[a-z0-9_/]+)", f.read_text(encoding="utf-8")))
        for tag in (DATA / "minecraft/tags/function").glob("*.json"):
            refs |= {v for v in json.loads(tag.read_text(encoding="utf-8"))["values"]
                     if v.startswith("rlm_spawn:")}
        self.assertIn("rlm_spawn:load", refs)
        self.assertIn("rlm_spawn:tick", refs)
        for ref in sorted(refs):
            with self.subTest(ref=ref):
                self.assertTrue(resource_path(ref, "function", ".mcfunction").is_file(), ref)

    def test_templates_exist(self):
        pool = json.loads((DATA / "rlm_spawn/worldgen/template_pool/spawn_lot.json").read_text(encoding="utf-8"))
        locations = [e["element"]["location"] for e in pool["elements"]]
        self.assertEqual(locations, ["rlm_spawn:lot"])
        refs = set(locations)
        for f in (DATA / "rlm_spawn/function").rglob("*.mcfunction"):
            refs |= set(re.findall(r"place template (\S+)", f.read_text(encoding="utf-8")))
        self.assertGreater(len(refs), 1)
        for ref in sorted(refs):
            with self.subTest(ref=ref):
                self.assertTrue(resource_path(ref, "structure", ".nbt").is_file(), ref)

    def test_worldgen_links(self):
        structure_set = json.loads((DATA / "rlm_spawn/worldgen/structure_set/spawn_lot.json").read_text(encoding="utf-8"))
        self.assertEqual(structure_set["structures"][0]["structure"], "rlm_spawn:spawn_lot")
        structure = json.loads((DATA / "rlm_spawn/worldgen/structure/spawn_lot.json").read_text(encoding="utf-8"))
        self.assertEqual(structure["biomes"], "#rlm_spawn:has_structure/spawn_lot")
        self.assertTrue(resource_path(structure["start_pool"], "worldgen/template_pool", ".json").is_file())
        # rayon max + noyau d'adaptation du terrain (12) <= 128
        self.assertLessEqual(structure["max_distance_from_center"] + 12, 128)
        tag = json.loads((DATA / "rlm_spawn/tags/worldgen/structure/spawn_lot.json").read_text(encoding="utf-8"))
        self.assertEqual(tag["values"], ["rlm_spawn:spawn_lot"])
        loot = json.loads((DATA / "rlm_spawn/loot_table/locate_lot.json").read_text(encoding="utf-8"))
        self.assertEqual(loot["pools"][0]["entries"][0]["functions"][0]["destination"], "rlm_spawn:spawn_lot")

    def test_single_biome(self):
        tag = json.loads((DATA / "rlm_spawn/tags/worldgen/biome/has_structure/spawn_lot.json").read_text(encoding="utf-8"))
        self.assertEqual(len(tag["values"]), 1)


if __name__ == "__main__":
    unittest.main()
