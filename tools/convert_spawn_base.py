"""Convertit le build de spawn (.litematic) en morceaux de structure vanilla
et génère les fonctions de pose.

Usage : python tools/convert_spawn_base.py
Réglages : tools/spawn_base.json
  litematic     chemin du .litematic (relatif à la racine du dépôt)
  ground_layer  couche du build posée au niveau du bloc de surface du terrain ;
                -1 = build posé juste au-dessus de la surface (eau, sol) sans la remplacer
  spawn         [x, y, z] du bloc où l'on apparaît (repère du build rogné)
  spawn_yaw     orientation du regard à l'apparition, en degrés
  foundation_depth  profondeur max du talus en escalier comblé sous le build
                (vide et eau seulement, un bloc vers l'extérieur par bloc de descente ;
                0 ou absent = pas de fondations)

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
MAX_FORCELOAD = 256          # chunks max d'une commande forceload
VERIFY_SAMPLES = 24
MAX_FOUNDATION = 64
MAX_FILL = 32768             # limite de blocs d'une commande fill
FOUNDATION_BLOCK = "minecraft:grass_block"   # l'herbe recouverte redevient terre d'elle-même
FOUNDATION_FILTER = "#minecraft:replaceable"
# Blocs renommés depuis les anciennes versions : le jeu les met à jour au chargement
# (on garde la DataVersion d'origine), la vérification doit donc chercher le nouveau nom.
RENAMED = {"minecraft:grass": "minecraft:short_grass", "minecraft:grass_path": "minecraft:dirt_path"}
ROTATIONS = ("none", "clockwise_90", "clockwise_180", "counterclockwise_90")
ROTATION_YAW = {"none": 0, "clockwise_90": 90, "clockwise_180": 180, "counterclockwise_90": -90}
# Valeur attendue par l'argument de rotation des commandes (place template).
COMMAND_ROTATION = {"none": "none", "clockwise_90": "clockwise_90", "clockwise_180": "180",
                    "counterclockwise_90": "counterclockwise_90"}


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
    if not -1 <= g < sy:
        raise ValueError("ground_layer %d hors limites (-1 à %d)" % (g, sy - 1))
    depth = config.get("foundation_depth", 0)
    if not 0 <= depth <= MAX_FOUNDATION:
        raise ValueError("foundation_depth %d hors limites (0 à %d)" % (depth, MAX_FOUNDATION))
    span = max(0, depth - 1)
    chunks = _chunk_span(sx + 2 * span) * _chunk_span(sz + 2 * span)
    if chunks > MAX_FORCELOAD:
        raise ValueError("build trop grand : %d x %d blocs + %d de fondations = jusqu'à %d chunks à charger, "
                         "%d au maximum" % (sx, sz, depth, chunks, MAX_FORCELOAD))
    x, y, z = config["spawn"]

    def air_at(y_):
        if not (0 <= x < sx and 0 <= z < sz and y_ >= 0):
            raise ValueError("point de spawn %r hors du build" % (config["spawn"],))
        return y_ >= sy or build.is_air(x, y_, z)
    if not (air_at(y) and air_at(y + 1)):
        raise ValueError("point de spawn %r : il faut de l'air sur 2 blocs de haut" % (config["spawn"],))
    if y == 0 or air_at(y - 1):
        raise ValueError("point de spawn %r : il faut un bloc solide en dessous" % (config["spawn"],))


def _chunk_span(length):
    """Nombre de chunks qu'une bande de `length` blocs peut toucher au pire."""
    return (length + 14) // 16 + 1


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


def _data_version(build):
    """Version d'origine si elle est plus ancienne : le jeu mettra à jour blocs et entités."""
    if 0 < build.data_version < DATA_VERSION:
        return build.data_version
    return DATA_VERSION


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
    return {"DataVersion": Int(_data_version(build)), "size": _int_list(size), "palette": palette,
            "blocks": blocks, "entities": entities}


def _footprint(build, rotation):
    """Boîte (x1, z1, x2, z2) occupée par le build tourné, relative à l'ancre."""
    sx, _, sz = build.size
    corners = [rotate_offset(x, z, rotation) for x in (0, sx - 1) for z in (0, sz - 1)]
    xs = [c[0] for c in corners]
    zs = [c[1] for c in corners]
    return min(xs), min(zs), max(xs), max(zs)


def _load_rect(build, rotation, depth):
    """Zone à charger avant la pose : emprise du build élargie du débord des fondations."""
    x1, z1, x2, z2 = _footprint(build, rotation)
    e = max(0, depth - 1)
    return x1 - e, z1 - e, x2 + e, z2 + e


def _steps(a, b):
    out = list(range(a, b + 1, 16))
    if out[-1] != b:
        out.append(b)
    return out


def _foundation_top(ground_layer):
    """Hauteur (relative à l'ancre) de la première couche de fondations."""
    return min(0, -ground_layer) - 1


def _foundation_lines(build, rotation, depth, ground_layer):
    """Talus en escalier sous le build : la couche j (1..depth) est j-1 blocs sous le haut
    des fondations, élargie de j-1."""
    x1, z1, x2, z2 = _footprint(build, rotation)
    top = _foundation_top(ground_layer)
    lines = []
    for j in range(1, depth + 1):
        e = j - 1
        ax, bx, az, bz = x1 - e, x2 + e, z1 - e, z2 + e
        width = max(1, MAX_FILL // (bz - az + 1))
        for sx0 in range(ax, bx + 1, width):
            sx1 = min(bx, sx0 + width - 1)
            lines.append("fill ~%d ~%d ~%d ~%d ~%d ~%d %s replace %s"
                         % (sx0, top - e, az, sx1, top - e, bz, FOUNDATION_BLOCK, FOUNDATION_FILTER))
    return lines


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
    _validate(build, config)
    _warn(build)

    g = config["ground_layer"]
    depth = config.get("foundation_depth", 0)
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
    # Exécutées à l'ancre : chargement forcé de la seule zone utile, selon la rotation.
    for rot in ROTATIONS:
        x1, z1, x2, z2 = _load_rect(build, rot, depth)
        write("forceload_" + rot, [header, "forceload add ~%d ~%d ~%d ~%d" % (x1, z1, x2, z2)])
        write("unforceload_" + rot, [header, "forceload remove ~%d ~%d ~%d ~%d" % (x1, z1, x2, z2)])
        area = [header] + ["execute unless loaded ~%d ~ ~%d run return fail" % (x, z)
                           for x in _steps(x1, x2) for z in _steps(z1, z2)]
        write("area_loaded_" + rot, area + ["return 1"])

    samples = _verify_samples(build, skip)
    spx, spy, spz = config["spawn"]
    for rot in ROTATIONS:
        lines = [header, 'data modify storage rlm_spawn:data lot.rotation set value "%s"' % rot]
        # Fondations d'abord : la pose du build réécrit ensuite ses propres pièces enterrées.
        lines += _foundation_lines(build, rot, depth, g)
        for name, (ox, oy, oz), _ in pieces:
            rx, rz = rotate_offset(ox, oz, rot)
            lines.append("place template rlm_spawn:base/%s ~%d ~%d ~%d %s" % (name, rx, oy - g, rz, COMMAND_ROTATION[rot]))
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
                          % (vx, y - g, vz, RENAMED.get(build.block_name(x, y, z), build.block_name(x, y, z))))
        if depth:
            fx1, fz1, fx2, fz2 = _footprint(build, rot)
            for cx, cz in ((fx1, fz1), (fx2, fz1), (fx1, fz2), (fx2, fz2)):
                verify.append("execute if block ~%d ~%d ~%d %s run return fail"
                              % (cx, _foundation_top(g), cz, FOUNDATION_FILTER))
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
