"""Chargement d'un fichier .litematic (Litematica) à une seule région.

Repère local : origine au coin minimal, indice d'un bloc (y*sz + z)*sx + x.
"""
from dataclasses import dataclass, field

from nbtio import read_nbt_file

AIR_NAMES = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air"}
_U64 = 0xFFFFFFFFFFFFFFFF


@dataclass
class Build:
    size: tuple                     # (sx, sy, sz)
    palette: list                   # compounds {"Name": str, "Properties"?: dict}
    blocks: list                    # indices de palette
    block_entities: dict = field(default_factory=dict)   # (x, y, z) -> NBT sans x/y/z
    entities: list = field(default_factory=list)         # ((x, y, z) flottants, NBT)
    data_version: int = 0

    def index(self, x, y, z) -> int:
        sx, _, sz = self.size
        return (y * sz + z) * sx + x

    def block_name(self, x, y, z) -> str:
        return self.palette[self.blocks[self.index(x, y, z)]]["Name"]

    def is_air(self, x, y, z) -> bool:
        return self.block_name(x, y, z) in AIR_NAMES


def _decode_states(longs, bits, count):
    mask = (1 << bits) - 1
    out = [0] * count
    for i in range(count):
        li, off = divmod(i * bits, 64)
        val = (longs[li] & _U64) >> off
        if off + bits > 64:
            val |= (longs[li + 1] & _U64) << (64 - off)
        out[i] = val & mask
    return out


def load_litematic(path) -> Build:
    root = read_nbt_file(path)
    regions = root.get("Regions", {})
    if len(regions) != 1:
        raise ValueError("le .litematic doit contenir exactement 1 région (il en a %d)" % len(regions))
    reg = next(iter(regions.values()))
    raw = [int(reg["Size"][k]) for k in "xyz"]
    sx, sy, sz = (abs(v) for v in raw)
    palette = list(reg["BlockStatePalette"])
    bits = max(2, (len(palette) - 1).bit_length())
    blocks = _decode_states(reg["BlockStates"], bits, sx * sy * sz)

    block_entities = {}
    for te in reg.get("TileEntities", []):
        nbt = {k: v for k, v in te.items() if k not in ("x", "y", "z")}
        block_entities[(int(te["x"]), int(te["y"]), int(te["z"]))] = nbt

    shift = [v + 1 if v < 0 else 0 for v in raw]
    entities = []
    for ent in reg.get("Entities", []):
        pos = tuple(float(p) - d for p, d in zip(ent["Pos"], shift))
        entities.append((pos, ent))

    return Build((sx, sy, sz), palette, blocks, block_entities, entities,
                 int(root.get("MinecraftDataVersion", 0)))


def trim(build: Build) -> Build:
    sx, sy, sz = build.size
    air = {i for i, p in enumerate(build.palette) if p["Name"] in AIR_NAMES}
    lo = [None, None, None]
    hi = [None, None, None]
    for i, v in enumerate(build.blocks):
        if v in air:
            continue
        x = i % sx
        z = (i // sx) % sz
        y = i // (sx * sz)
        for a, c in enumerate((x, y, z)):
            lo[a] = c if lo[a] is None else min(lo[a], c)
            hi[a] = c if hi[a] is None else max(hi[a], c)
    if lo[0] is None:
        raise ValueError("le build est vide")
    nx, ny, nz = (hi[a] - lo[a] + 1 for a in range(3))
    ox, oy, oz = lo
    blocks = [build.blocks[build.index(x + ox, y + oy, z + oz)]
              for y in range(ny) for z in range(nz) for x in range(nx)]
    block_entities = {(x - ox, y - oy, z - oz): nbt for (x, y, z), nbt in build.block_entities.items()
                      if 0 <= x - ox < nx and 0 <= y - oy < ny and 0 <= z - oz < nz}
    entities = []
    for (x, y, z), nbt in build.entities:
        p = (x - ox, y - oy, z - oz)
        if 0 <= p[0] < nx and 0 <= p[1] < ny and 0 <= p[2] < nz:
            entities.append((p, nbt))
    return Build((nx, ny, nz), build.palette, blocks, block_entities, entities, build.data_version)
