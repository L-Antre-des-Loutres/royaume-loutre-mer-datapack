"""Convertit le build de spawn (.litematic) en morceaux de structure vanilla
et génère les fonctions de pose.

Usage : python tools/convert_spawn_base.py
Réglages : tools/spawn_base.json
  litematic     chemin du .litematic (relatif à la racine du dépôt)
  ground_layer  couche du build posée au niveau du bloc de surface du terrain
  spawn         [x, y, z] du bloc où l'on apparaît (repère du build rogné)
  spawn_yaw     orientation du regard à l'apparition, en degrés

Fichiers régénérés (ne pas éditer à la main) :
  data/rlm_spawn/structure/lot.nbt
  data/rlm_spawn/structure/base/*.nbt
  data/rlm_spawn/function/generated/*.mcfunction
"""
import json
import shutil
import sys
from collections import deque
from pathlib import Path

from litematic import AIR_NAMES, load_litematic, trim
from nbtio import Double, Float, Int, write_nbt_file

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_VERSION = 3955          # Minecraft 1.21.1
MAX_PIECE = 48
MAX_REACH = 224
VERIFY_SAMPLES = 24
ROTATIONS = ("none", "clockwise_90", "clockwise_180", "counterclockwise_90")
ROTATION_YAW = {"none": 0, "clockwise_90": 90, "clockwise_180": 180, "counterclockwise_90": -90}


def split_axis(n: int) -> list:
    k = -(-n // MAX_PIECE)
    base, extra = divmod(n, k)
    out, start = [], 0
    for i in range(k):
        length = base + (1 if i < extra else 0)
        out.append((start, length))
        start += length
    return out


def rotate_offset(x: int, z: int, rotation: str) -> tuple:
    return {"none": (x, z), "clockwise_90": (-z, x),
            "clockwise_180": (-x, -z), "counterclockwise_90": (z, -x)}[rotation]


def _yaw(spawn_yaw, rotation):
    y = (spawn_yaw + ROTATION_YAW[rotation]) % 360
    if y > 180:
        y -= 360
    return int(y) if float(y).is_integer() else y


def _exterior_buried_air(build, ground_layer) -> set:
    """Air sous ground_layer relié à une face latérale ou au fond de la boîte."""
    sx, _, sz = build.size
    seen = set()
    queue = deque()
    for y in range(ground_layer):
        for z in range(sz):
            for x in range(sx):
                if (y == 0 or x in (0, sx - 1) or z in (0, sz - 1)) and build.is_air(x, y, z):
                    seen.add((x, y, z))
                    queue.append((x, y, z))
    while queue:
        x, y, z = queue.popleft()
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            n = (x + dx, y + dy, z + dz)
            if (0 <= n[0] < sx and 0 <= n[1] < ground_layer and 0 <= n[2] < sz
                    and n not in seen and build.is_air(*n)):
                seen.add(n)
                queue.append(n)
    return seen


def _validate(build, config):
    sx, sy, sz = build.size
    g = config["ground_layer"]
    if not 0 <= g < sy:
        raise ValueError("ground_layer %d hors du build (0 à %d)" % (g, sy - 1))
    reach = -(-max(sx, sz) // 16) * 16
    if reach > MAX_REACH:
        raise ValueError("build trop grand : %d x %d blocs, %d au maximum de côté" % (sx, sz, MAX_REACH))
    x, y, z = config["spawn"]

    def air_at(y_):
        if not (0 <= x < sx and 0 <= z < sz and y_ >= 0):
            raise ValueError("point de spawn %r hors du build" % (config["spawn"],))
        return y_ >= sy or build.is_air(x, y_, z)
    if not (air_at(y) and air_at(y + 1)):
        raise ValueError("point de spawn %r : il faut de l'air sur 2 blocs de haut" % (config["spawn"],))
    if y == 0 or air_at(y - 1):
        raise ValueError("point de spawn %r : il faut un bloc solide en dessous" % (config["spawn"],))
    return reach


def _warn(build):
    names = sorted({build.palette[i]["Name"] for i in set(build.blocks)} - AIR_NAMES)
    foreign = [n for n in names if not n.startswith("minecraft:")]
    if foreign:
        print("Attention : blocs hors Minecraft vanilla (le mod doit être dans le pack) : "
              + ", ".join(foreign), file=sys.stderr)
    if build.data_version > DATA_VERSION:
        print("Attention : build fait avec une version plus récente (DataVersion %d > %d, 1.21.1). "
              "Vérifier que ces blocs existent en 1.21.1 : %s"
              % (build.data_version, DATA_VERSION, ", ".join(names)), file=sys.stderr)


def _int_list(values):
    return [Int(v) for v in values]


def _piece(build, origin, size, skip):
    ox, oy, oz = origin
    lx, ly, lz = size
    palette, keys, blocks = [], {}, []
    for y in range(ly):
        for z in range(lz):
            for x in range(lx):
                p = (x + ox, y + oy, z + oz)
                if p in skip:
                    continue
                state = build.palette[build.blocks[build.index(*p)]]
                key = repr(state)
                if key not in keys:
                    keys[key] = len(palette)
                    palette.append(state)
                entry = {"pos": _int_list((x, y, z)), "state": Int(keys[key])}
                if p in build.block_entities:
                    entry["nbt"] = build.block_entities[p]
                blocks.append(entry)
    entities = []
    for (ex, ey, ez), nbt in build.entities:
        if ox <= ex < ox + lx and oy <= ey < oy + ly and oz <= ez < oz + lz:
            rel = (ex - ox, ey - oy, ez - oz)
            entities.append({"pos": [Double(c) for c in rel],
                             "blockPos": _int_list(int(c // 1) for c in rel),
                             "nbt": {k: v for k, v in nbt.items() if k != "UUID"}})
    return {"DataVersion": Int(DATA_VERSION), "size": _int_list(size), "palette": palette,
            "blocks": blocks, "entities": entities}


def _verify_samples(build, skip):
    sx, sy, sz = build.size
    cells = [(x, y, z) for y in range(sy) for z in range(sz) for x in range(sx)
             if (x, y, z) not in skip and not build.is_air(x, y, z)]
    if len(cells) <= VERIFY_SAMPLES:
        return cells
    step = len(cells) / VERIFY_SAMPLES
    return [cells[int(i * step)] for i in range(VERIFY_SAMPLES)]


def convert(config: dict, out_root: Path) -> None:
    out_root = Path(out_root)
    src = Path(config["litematic"])
    if not src.is_absolute():
        src = REPO_ROOT / src
    build = trim(load_litematic(src))
    reach = _validate(build, config)
    _warn(build)

    g = config["ground_layer"]
    sx, sy, sz = build.size
    skip = _exterior_buried_air(build, g)
    pieces = []
    for iy, (oy, ly) in enumerate(split_axis(sy)):
        for iz, (oz, lz) in enumerate(split_axis(sz)):
            for ix, (ox, lx) in enumerate(split_axis(sx)):
                pieces.append(("p_%d_%d_%d" % (ix, iy, iz), (ox, oy, oz),
                               _piece(build, (ox, oy, oz), (lx, ly, lz), skip)))

    structure = out_root / "data/rlm_spawn/structure"
    base_dir = structure / "base"
    gen = out_root / "data/rlm_spawn/function/generated"
    for d in (base_dir, gen):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)

    for name, _, nbt in pieces:
        write_nbt_file(base_dir / (name + ".nbt"), nbt)
    write_nbt_file(structure / "lot.nbt", {
        "DataVersion": Int(DATA_VERSION), "size": _int_list((sx, sy - g, sz)),
        "palette": [], "blocks": [],
        "entities": [{"pos": [Double(0.5), Double(0.0), Double(0.5)], "blockPos": _int_list((0, 0, 0)),
                      "nbt": {"id": "minecraft:marker", "Tags": ["rlm_spawn.anchor"],
                              "Rotation": [Float(0.0), Float(0.0)]}}]})

    def write(name, lines):
        (gen / (name + ".mcfunction")).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    header = "# Généré par tools/convert_spawn_base.py : ne pas éditer."
    write("constants", [header, "scoreboard players set #reach rlm_spawn %d" % reach])
    area = [header]
    for dx in range(-reach, reach + 1, 16):
        for dz in range(-reach, reach + 1, 16):
            area.append("execute unless loaded ~%d ~ ~%d run return fail" % (dx, dz))
    write("area_loaded", area + ["return 1"])

    samples = _verify_samples(build, skip)
    spx, spy, spz = config["spawn"]
    for rot in ROTATIONS:
        lines = [header, 'data modify storage rlm_spawn:data lot.rotation set value "%s"' % rot]
        for name, (ox, oy, oz), _ in pieces:
            rx, rz = rotate_offset(ox, oz, rot)
            lines.append("place template rlm_spawn:base/%s ~%d ~%d ~%d %s" % (name, rx, oy - g, rz, rot))
        rx, rz = rotate_offset(spx, spz, rot)
        lines.append("data modify storage rlm_spawn:data spawn.yaw set value %s" % _yaw(config["spawn_yaw"], rot))
        lines.append("execute positioned ~%d ~%d ~%d run function rlm_spawn:step/set_spawn "
                     "with storage rlm_spawn:data spawn" % (rx, spy - g, rz))
        lines.append("execute store result score #verified rlm_spawn run function "
                     "rlm_spawn:generated/verify_%s" % rot)
        write("place_" + rot, lines)

        verify = [header]
        for x, y, z in samples:
            vx, vz = rotate_offset(x, z, rot)
            verify.append("execute unless block ~%d ~%d ~%d %s run return fail"
                          % (vx, y - g, vz, build.block_name(x, y, z)))
        write("verify_" + rot, verify + ["return 1"])


def main() -> int:
    config = json.loads((REPO_ROOT / "tools/spawn_base.json").read_text(encoding="utf-8"))
    try:
        convert(config, REPO_ROOT)
    except ValueError as e:
        print("Erreur : %s" % e, file=sys.stderr)
        return 1
    print("Build converti : data/rlm_spawn/structure/ et data/rlm_spawn/function/generated/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
