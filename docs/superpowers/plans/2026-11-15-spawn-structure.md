# Spawn dans une structure unique — plan de réalisation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** À chaque nouveau monde, poser un build unique dans un biome précis, terrain raccordé, et y faire apparaître tous les joueurs.

**Architecture:** Un script Python convertit un `.litematic` en morceaux de structure vanilla et génère les fonctions de pose. Une structure de génération vide (« repère ») prépare le terrain dans le biome choisi et contient une entité ancre. Au premier chargement d'un monde neuf, une machine à états en `mcfunction` localise le repère le plus proche de 0,0 via une carte d'exploration, charge la zone, pose les morceaux sur l'ancre, fixe le spawn et téléporte les joueurs.

**Tech Stack:** Datapack Minecraft 1.21.1 (`pack_format` 48, dossiers au singulier), jar Fabric sans code, Python 3 stdlib uniquement (`unittest`, pas de dépendance).

**Spec:** `docs/superpowers/specs/2026-11-15-spawn-structure-design.md`

## Global Constraints

- Minecraft 1.21.1, `DataVersion` des structures écrites : `3955`.
- Espace de noms du datapack : `rlm_spawn`. Id du mod Fabric : `royaume-loutre-mer-datapack`.
- Biome provisoire : `minecraft:plains`, dans un seul fichier de tag.
- Python : stdlib uniquement. Tests : `python -m unittest discover -s tools/tests -v` depuis la racine du dépôt.
- Fichiers sous `data/rlm_spawn/structure/` et `data/rlm_spawn/function/generated/` : générés, jamais édités à la main.
- Travail sur la branche `spawn-structure`. Commits locaux en français. **Aucun `git push`.**
- Ne pas toucher à `data/cobblemon/`, `pack.mcmeta`, `LICENSE`, ni au dépôt voisin `royaume-loutre-mer-trainers`.
- Java pour les tests serveur : `C:/Users/Perodeau/AppData/Roaming/ModrinthApp/meta/java_versions/zulu21.52.203-ca-jre21.0.12.1-win_x64/bin/java.exe`.

## Review Focus

1. **Biome introuvable dans le rayon de recherche** : le spawn reste normal, les joueurs sont prévenus, aucun chunk ne reste chargé de force. → Tâche 6, mode `--biome minecraft:the_void`.
2. **Monde déjà existant auquel on ajoute le jar** : rien ne bouge, ni spawn ni structure. → Tâche 6, mode `--existing-world`.
3. **Build avec blocs moddés ou d'une version plus récente** : le convertisseur avertit en listant les blocs concernés, sans échouer. → Tâche 4, `test_warns_on_foreign_blocks`.
4. **Build trop grand ou à plusieurs régions** : erreur claire, aucun fichier écrit. → Tâche 3 (`test_rejects_multi_region`) et Tâche 4 (`test_rejects_oversized_build`).
5. **Joueur présent avant la fin de la pose, déconnexion/reconnexion, mort sans lit sous un toit** : téléporté une seule fois à l'arrivée, renvoyé à l'intérieur après une mort sans lit, jamais re-téléporté à la reconnexion. Non testable sans client → liste de vérification en jeu, Tâche 7.

## Structure des fichiers

```
fabric.mod.json                                   mod Fabric sans code
.gitignore                                        build/, tools/.server/, __pycache__/
README.md                                         mode d'emploi
tools/spawn_base.json                             réglages du build
tools/source/base.litematic                       build source (base de test)
tools/nbtio.py                                    lecture/écriture NBT gzip typé
tools/litematic.py                                .litematic -> Build
tools/convert_spawn_base.py                       Build -> structures + fonctions générées
tools/build_jar.py                                assemble le jar
tools/server_test.py                              test sur serveur sans interface
tools/tests/test_*.py
data/minecraft/tags/function/{load,tick}.json
data/rlm_spawn/function/*.mcfunction              machine à états (écrite à la main)
data/rlm_spawn/function/step/*.mcfunction
data/rlm_spawn/function/generated/*.mcfunction    généré
data/rlm_spawn/structure/lot.nbt                  généré : repère vide + ancre
data/rlm_spawn/structure/base/p_<ix>_<iy>_<iz>.nbt  généré : morceaux du build
data/rlm_spawn/loot_table/locate_lot.json
data/rlm_spawn/worldgen/{structure,structure_set,template_pool}/spawn_lot.json
data/rlm_spawn/tags/worldgen/biome/has_structure/spawn_lot.json   <- le biome
data/rlm_spawn/tags/worldgen/structure/spawn_lot.json
```

Repère de coordonnées « local » utilisé partout : origine au coin minimal du build **après rognage** des couches vides, `x`/`z` horizontaux, `y` vers le haut. Indice d'un bloc : `(y * sz + z) * sx + x`.

---

### Task 1: Dépôt prêt à livrer un jar

**Files:**
- Create: `.gitignore`, `fabric.mod.json`, `tools/build_jar.py`, `tools/tests/test_build_jar.py`

**Interfaces:**
- Produces: `build_jar(repo_root: Path, out_dir: Path) -> Path` ; nom du jar `royaume-loutre-mer-datapack-<version>.jar`, version lue dans `fabric.mod.json`. Exécutable : `python tools/build_jar.py` écrit dans `build/`.

- [ ] **Step 1:** `git switch -c spawn-structure`, puis commit des deux documents sous `docs/superpowers/`.
- [ ] **Step 2: Test en échec** — `tools/tests/test_build_jar.py` :

```python
def test_jar_contains_only_pack_files(self):
    jar = build_jar(REPO_ROOT, Path(self.tmp))
    names = set(zipfile.ZipFile(jar).namelist())
    self.assertEqual(jar.name, "royaume-loutre-mer-datapack-0.1.0.jar")
    self.assertIn("fabric.mod.json", names)
    self.assertIn("pack.mcmeta", names)
    self.assertIn("data/cobblemon/starters/default.json", names)
    self.assertFalse([n for n in names if n.startswith(("tools/", "docs/", ".git", ".idea", "build/"))])
```

- [ ] **Step 3:** Lancer les tests, attendu : échec à l'import de `build_jar`.
- [ ] **Step 4:** Écrire `fabric.mod.json` (ci-dessous), `.gitignore` (`build/`, `tools/.server/`, `__pycache__/`) et `build_jar` : zippe `fabric.mod.json`, `pack.mcmeta`, `LICENSE` et tout `data/`, chemins avec `/`.

```json
{
  "schemaVersion": 1,
  "id": "royaume-loutre-mer-datapack",
  "version": "0.1.0",
  "name": "Datapack Royaume de Loutre Mer",
  "environment": "*"
}
```

- [ ] **Step 5:** Tests verts, puis commit `Prépare la livraison du datapack en jar Fabric`.

### Task 2: Lecture et écriture NBT

**Files:**
- Create: `tools/nbtio.py`, `tools/tests/test_nbtio.py`

**Interfaces:**
- Produces: `read_nbt_file(path) -> dict`, `write_nbt_file(path, root: dict) -> None` (gzip, nom racine vide). Types conservés par des classes : `Byte`, `Short`, `Int`, `Long` (sous-classes de `int`), `Float`, `Double` (sous-classes de `float`), `ByteArray`, `IntArray`, `LongArray` (sous-classes de `list`) ; `str`, `dict` et `list` pour chaîne, compound et liste. Une liste vide s'écrit avec le type d'élément `TAG_End`. `LongArray` contient des entiers **non signés** (0 à 2^64-1) à la lecture.

- [ ] **Step 1: Tests en échec** :

```python
def test_round_trip_keeps_types(self):
    root = {"b": Byte(-3), "s": Short(7), "i": Int(3955), "l": Long(2**40), "f": Float(0.5),
            "d": Double(1.25), "t": "é", "list": [Int(1), Int(2)], "empty": [],
            "c": {"n": [Double(0.5)]}, "ia": IntArray([1, -2]), "la": LongArray([2**64 - 1])}
    write_nbt_file(p, root); back = read_nbt_file(p)
    self.assertEqual(back, root)
    for k in root: self.assertIs(type(back[k]), type(root[k]))

def test_reads_test_litematic(self):
    root = read_nbt_file(REPO_ROOT / "tools/source/base.litematic")
    self.assertEqual(root["MinecraftDataVersion"], 4438)
    self.assertEqual(root["Metadata"]["TotalBlocks"], 27660)
```

- [ ] **Step 2:** Copier `C:/Users/Perodeau/Downloads/Cobblemon base principal.litematic` vers `tools/source/base.litematic`. Lancer, attendu : échec à l'import.
- [ ] **Step 3:** Implémenter `tools/nbtio.py` (big-endian, UTF-8).
- [ ] **Step 4:** Tests verts, commit `Ajoute la lecture/écriture NBT et la base de test`.

### Task 3: Chargement du `.litematic`

**Files:**
- Create: `tools/litematic.py`, `tools/tests/test_litematic.py`

**Interfaces:**
- Consumes: `nbtio.read_nbt_file`.
- Produces:

```python
@dataclass
class Build:
    size: tuple[int, int, int]            # (sx, sy, sz)
    palette: list[dict]                   # compounds {"Name": str, "Properties"?: dict}
    blocks: list[int]                     # indices de palette, ordre (y*sz + z)*sx + x
    block_entities: dict[tuple[int, int, int], dict]   # position locale -> NBT sans x/y/z
    entities: list[tuple[tuple[float, float, float], dict]]  # position locale -> NBT
    data_version: int
    def block_name(self, x, y, z) -> str

def load_litematic(path) -> Build     # lève ValueError si le fichier n'a pas exactement 1 région
def trim(build: Build) -> Build       # rogne à la boîte englobante des blocs non-air
```

Règles de décodage (non déductibles des tests) :
- Tailles : valeur absolue de `Size`. `BlockStates` : `bits = max(2, (len(palette) - 1).bit_length())`, entrées **collées sans alignement** (une entrée peut chevaucher deux longs), indice `(y*sz + z)*sx + x` depuis le coin minimal.
- `TileEntities` : `x`,`y`,`z` déjà relatifs au coin minimal ; les retirer du NBT.
- `Entities` : `Pos` est relatif au coin `Position` de la région, pas au coin minimal. Position locale = `Pos - d` avec, par axe, `d = Size + 1` si `Size < 0`, sinon `0`. Non vérifiable sur la base de test (aucune entité) : couvert par un fichier synthétique.
- `trim` décale aussi `block_entities` et `entities`, et écarte les entités hors boîte.

- [ ] **Step 1: Tests en échec** :

```python
def test_loads_test_base(self):
    b = load_litematic(SRC)
    self.assertEqual(b.size, (82, 87, 81)); self.assertEqual(b.data_version, 4438)
    self.assertEqual(sum(1 for i in b.blocks if b.palette[i]["Name"] != "minecraft:air"), 27660)
    self.assertEqual(b.block_name(41, 0, 40), "minecraft:oak_planks")
    self.assertEqual(b.block_name(41, 28, 40), "minecraft:glass")

def test_trim_drops_empty_top_layers(self):
    t = trim(load_litematic(SRC))
    self.assertEqual(t.size, (82, 60, 81)); self.assertEqual(t.block_name(41, 0, 40), "minecraft:oak_planks")

def test_negative_size_entities_and_block_entities(self):
    # fichier synthétique écrit avec nbtio : Size (-3, 2, 2), Position (10, 5, 5),
    # un coffre à l'indice local (2, 0, 1), une entité avec Pos (-1.5, 0.0, 0.5)
    self.assertEqual(b.size, (3, 2, 2))
    self.assertIn((2, 0, 1), b.block_entities); self.assertNotIn("x", b.block_entities[(2, 0, 1)])
    self.assertEqual(b.entities[0][0], (0.5, 0.0, 0.5))

def test_rejects_multi_region(self):
    with self.assertRaisesRegex(ValueError, "1 région"): load_litematic(two_region_file)
```

- [ ] **Step 2:** Lancer, attendu : échec à l'import.
- [ ] **Step 3:** Implémenter.
- [ ] **Step 4:** Tests verts, commit `Charge et rogne les fichiers .litematic`.

### Task 4: Convertisseur

**Files:**
- Create: `tools/convert_spawn_base.py`, `tools/spawn_base.json`, `tools/tests/test_convert.py`
- Generated (committés) : `data/rlm_spawn/structure/lot.nbt`, `data/rlm_spawn/structure/base/*.nbt`, `data/rlm_spawn/function/generated/*.mcfunction`

**Interfaces:**
- Consumes: `litematic.load_litematic`, `litematic.trim`, `nbtio.write_nbt_file`.
- Produces: `python tools/convert_spawn_base.py` lit `tools/spawn_base.json` et régénère les fichiers ci-dessus (il vide d'abord `structure/base/` et `function/generated/`). Fonctions générées, toutes exécutées **positionnées sur le bloc de l'ancre, alignées** :
  - `rlm_spawn:generated/constants` — `scoreboard players set #reach rlm_spawn <R>`
  - `rlm_spawn:generated/area_loaded` — renvoie 1 si toute la zone est chargée, sinon échoue
  - `rlm_spawn:generated/place_<rotation>` pour `none`, `clockwise_90`, `clockwise_180`, `counterclockwise_90`
  - `rlm_spawn:generated/verify_<rotation>` — renvoie 1 si un échantillon de blocs est en place

`tools/spawn_base.json` (coordonnées dans le repère local rogné) :

```json
{ "litematic": "tools/source/base.litematic", "ground_layer": 0, "spawn": [41, 1, 40], "spawn_yaw": 0 }
```

`ground_layer` = indice de la couche du build qui remplace le bloc de surface du terrain ; les couches en dessous sont enterrées.

Décisions :
- `split_axis(n) -> list[tuple[int, int]]` (début, longueur) : `k = ceil(n / 48)` morceaux, longueurs les plus égales possible, les plus longues d'abord. `81 -> [(0, 41), (41, 40)]`.
- Morceau `p_<ix>_<iy>_<iz>` : format structure vanilla (`DataVersion`, `size`, `palette`, `blocks[{pos, state, nbt?}]`, `entities[{pos, blockPos, nbt}]`). Palette propre à chaque morceau.
- **Air** : couches `y >= ground_layer`, tout l'air est écrit (il dégage le terrain). Couches `y < ground_layer`, l'air « extérieur » est omis pour laisser le terrain en place : c'est l'air relié par des cases d'air, en restant sous `ground_layer`, à une face latérale ou au fond de la boîte. L'air enfermé (caves) est écrit.
- `rotate_offset(x, z, rotation)` : `none (x, z)`, `clockwise_90 (-z, x)`, `clockwise_180 (-x, -z)`, `counterclockwise_90 (z, -x)`.
- Ligne de pose d'un morceau d'origine locale `(ox, oy, oz)` : `place template rlm_spawn:base/p_i_j_k ~<rx> ~<oy - ground_layer> ~<rz> <rotation>` avec `(rx, rz) = rotate_offset(ox, oz)`. Toujours écrire le nombre (`~0`).
- `place_<rotation>` contient, dans l'ordre : `data modify storage rlm_spawn:data lot.rotation set value "<rotation>"` ; une ligne par morceau ; `data modify storage rlm_spawn:data spawn.yaw set value <yaw>` ; `execute positioned ~<rx> ~<sy - ground_layer> ~<rz> run function rlm_spawn:step/set_spawn with storage rlm_spawn:data spawn` ; `execute store result score #verified rlm_spawn run function rlm_spawn:generated/verify_<rotation>`.
- `yaw` = `spawn_yaw` + `0 / 90 / 180 / -90` selon la rotation, ramené dans `]-180, 180]`.
- `verify_<rotation>` : jusqu'à 24 blocs non-air répartis régulièrement, une ligne `execute unless block ~x ~y ~z <id> run return fail` chacun, puis `return 1`.
- `R` (portée) = `max(sx, sz)` arrondi au multiple de 16 supérieur. `area_loaded` : pour `dx`, `dz` de `-R` à `R` par pas de 16, `execute unless loaded ~<dx> ~ ~<dz> run return fail`, puis `return 1`.
- `lot.nbt` : `size [sx, sy - ground_layer, sz]`, `blocks []`, `palette []`, une entité `{pos: [0.5, 0.0, 0.5], blockPos: [0, 0, 0], nbt: {id: "minecraft:marker", Tags: ["rlm_spawn.anchor"], Rotation: [0f, 0f]}}`.
- Erreurs (`ValueError`, aucun fichier écrit) : `R > 224` ; point de spawn dont le bloc ou celui du dessus n'est pas de l'air, ou dont le bloc du dessous est de l'air ; `ground_layer` hors du build.
- Avertissements (stderr, sans échec) : blocs hors espace `minecraft:` ; `data_version > 3955`, avec la liste des noms de blocs à vérifier.

- [ ] **Step 1: Tests en échec** :

```python
def test_split_axis(self):
    self.assertEqual(split_axis(81), [(0, 41), (41, 40)])
    self.assertEqual(split_axis(48), [(0, 48)]); self.assertEqual(split_axis(49), [(0, 25), (25, 24)])

def test_rotate_offset(self):
    self.assertEqual(rotate_offset(3, 5, "clockwise_90"), (-5, 3))
    self.assertEqual(rotate_offset(3, 5, "clockwise_180"), (-3, -5))
    self.assertEqual(rotate_offset(3, 5, "counterclockwise_90"), (5, -3))

def test_converts_test_base(self):            # convert(config, out_root=tmp)
    names = sorted(p.stem for p in (tmp / "data/rlm_spawn/structure/base").glob("*.nbt"))
    self.assertEqual(len(names), 8)
    p = read_nbt_file(tmp / "data/rlm_spawn/structure/base/p_1_0_1.nbt")
    self.assertEqual(list(p["size"]), [41, 30, 40]); self.assertEqual(p["DataVersion"], 3955)
    # somme des blocs non-air des 8 morceaux == 27660
    lot = read_nbt_file(tmp / "data/rlm_spawn/structure/lot.nbt")
    self.assertEqual(list(lot["size"]), [82, 60, 81]); self.assertEqual(lot["entities"][0]["nbt"]["Tags"], ["rlm_spawn.anchor"])
    place = (tmp / "data/rlm_spawn/function/generated/place_clockwise_90.mcfunction").read_text()
    self.assertIn("place template rlm_spawn:base/p_1_0_1 ~-41 ~0 ~41 clockwise_90", place)
    self.assertIn("spawn.yaw set value 90", place)
    self.assertIn("execute positioned ~-40 ~1 ~41 run function rlm_spawn:step/set_spawn", place)
    self.assertIn("#reach rlm_spawn 96", (… / "constants.mcfunction").read_text())
    self.assertEqual((… / "area_loaded.mcfunction").read_text().count("unless loaded"), 169)

def test_buried_exterior_air_is_omitted(self):
    # build 5x3x5, ground_layer 2 : anneau de pierre fermé sur y=0..1 autour d'une case d'air centrale
    # -> l'air central (enfermé) est écrit, l'air hors de l'anneau sous y=2 est omis, l'air en y=2 est écrit

def test_block_entity_lands_in_its_piece(self):   # NBT du coffre présent dans blocks[].nbt, sans x/y/z
def test_rejects_oversized_build(self):           # sx = 230 -> ValueError mentionnant 224, aucun fichier écrit
def test_rejects_spawn_inside_block(self):        # spawn [41, 0, 40] -> ValueError
def test_warns_on_foreign_blocks(self):           # palette avec "chipped:x" et data_version 4438 -> stderr les nomme, pas d'exception
```

- [ ] **Step 2:** Lancer, attendu : échec à l'import.
- [ ] **Step 3:** Implémenter `convert(config: dict, out_root: Path) -> None` et le `main()`.
- [ ] **Step 4:** Tests verts. Lancer `python tools/convert_spawn_base.py` ; attendu : 8 fichiers dans `structure/base/`, `lot.nbt`, 10 fonctions générées, et l'avertissement sur la version 4438.
- [ ] **Step 5:** Commit `Convertit la base de test en morceaux de structure`.

### Task 5: Repère de génération et machine à états

**Files:**
- Create: les fichiers `worldgen/`, `tags/`, `loot_table/`, `function/` listés plus haut (hors `generated/`), `tools/tests/test_datapack.py`

**Interfaces:**
- Consumes: fonctions `rlm_spawn:generated/*` et structure `rlm_spawn:lot` de la Tâche 4.
- Produces: objectif `rlm_spawn` (joueur fictif `#state` : `1` localise, `2` attend la zone, `3` terminé, `-1` monde existant ignoré, `-2` échec ; `#verified` : 1 si l'échantillon est en place) ; stockage `rlm_spawn:data` : `lot {x, z, x1, z1, x2, z2, rotation}`, `spawn {x, y, z, yaw}`.

- [ ] **Step 1: Test en échec** — `tools/tests/test_datapack.py` : tout `.json` sous `data/` se parse ; toute fonction `rlm_spawn:…` appelée dans un `.mcfunction` ou un tag existe ; le `location` du template pool et les morceaux cités par `place template` existent en `.nbt` ; le tag de biome contient exactement une valeur.
- [ ] **Step 2:** Lancer, attendu : échec (fonction `rlm_spawn:step/set_spawn` introuvable).
- [ ] **Step 3: Génération** — écrire :

`worldgen/structure/spawn_lot.json`
```json
{ "type": "minecraft:jigsaw", "biomes": "#rlm_spawn:has_structure/spawn_lot", "step": "surface_structures",
  "terrain_adaptation": "beard_box", "spawn_overrides": {}, "start_pool": "rlm_spawn:spawn_lot", "size": 1,
  "start_height": { "absolute": 0 }, "project_start_to_heightmap": "WORLD_SURFACE_WG",
  "max_distance_from_center": 116, "use_expansion_hack": false }
```
`worldgen/template_pool/spawn_lot.json`
```json
{ "fallback": "minecraft:empty", "elements": [ { "weight": 1, "element": {
  "element_type": "minecraft:single_pool_element", "location": "rlm_spawn:lot",
  "projection": "rigid", "processors": "minecraft:empty" } } ] }
```
`worldgen/structure_set/spawn_lot.json`
```json
{ "structures": [ { "structure": "rlm_spawn:spawn_lot", "weight": 1 } ],
  "placement": { "type": "minecraft:random_spread", "spacing": 64, "separation": 32, "salt": 1712071125 } }
```
`tags/worldgen/biome/has_structure/spawn_lot.json` : `{ "values": ["minecraft:plains"] }`
`tags/worldgen/structure/spawn_lot.json` : `{ "values": ["rlm_spawn:spawn_lot"] }`
`loot_table/locate_lot.json`
```json
{ "type": "minecraft:chest", "pools": [ { "rolls": 1, "entries": [ { "type": "minecraft:item", "name": "minecraft:map",
  "functions": [ { "function": "minecraft:exploration_map", "destination": "rlm_spawn:spawn_lot",
    "decoration": "minecraft:red_x", "zoom": 2, "search_radius": 30, "skip_existing_chunks": false } ] } ] } ] }
```

- [ ] **Step 4: Fonctions** — tags `minecraft:load` -> `rlm_spawn:load`, `minecraft:tick` -> `rlm_spawn:tick`, puis :

`load`
```mcfunction
scoreboard objectives add rlm_spawn dummy
scoreboard objectives add rlm_spawn.deaths deathCount
execute unless score #state rlm_spawn matches -2147483648..2147483647 run function rlm_spawn:init
```
`init`
```mcfunction
execute store result score #age rlm_spawn run time query gametime
scoreboard players set #state rlm_spawn -1
execute if score #age rlm_spawn matches ..599 run function rlm_spawn:start
```
`start`
```mcfunction
scoreboard players set #state rlm_spawn 1
scoreboard players set #timer rlm_spawn 0
scoreboard players set #c360 rlm_spawn 360
function rlm_spawn:generated/constants
execute in minecraft:overworld run forceload add 0 0
```
`tick`
```mcfunction
execute if score #state rlm_spawn matches 1 in minecraft:overworld run function rlm_spawn:step/locate
execute if score #state rlm_spawn matches 2 in minecraft:overworld run function rlm_spawn:step/wait_area with storage rlm_spawn:data lot
execute if score #state rlm_spawn matches 3 as @a[tag=!rlm_spawn.arrived] run function rlm_spawn:arrive with storage rlm_spawn:data spawn
execute if score #state rlm_spawn matches 3 as @e[type=minecraft:player,scores={rlm_spawn.deaths=1..}] run function rlm_spawn:respawned
execute if score #state rlm_spawn matches -2 as @a[tag=!rlm_spawn.warned] run function rlm_spawn:warn
```
`step/locate`
```mcfunction
scoreboard players add #timer rlm_spawn 1
execute if score #timer rlm_spawn matches 1200.. run return run function rlm_spawn:fail
execute unless loaded 0 0 0 run return 0
scoreboard players set #found rlm_spawn 0
execute positioned 0.0 0 0.0 run loot spawn 0 300 0 loot rlm_spawn:locate_lot
execute as @e[type=minecraft:item,x=0,y=300,z=0,distance=..4,limit=1] run function rlm_spawn:step/read_map
kill @e[type=minecraft:item,x=0,y=300,z=0,distance=..4]
forceload remove 0 0
execute if score #found rlm_spawn matches 0 run return run function rlm_spawn:fail
function rlm_spawn:step/forceload_area with storage rlm_spawn:data lot
scoreboard players set #timer rlm_spawn 0
scoreboard players set #state rlm_spawn 2
```
`step/read_map` (exécutée par l'objet carte)
```mcfunction
execute unless data entity @s Item.components."minecraft:map_decorations"."+" run return 0
execute store result score #x rlm_spawn run data get entity @s Item.components."minecraft:map_decorations"."+".x
execute store result score #z rlm_spawn run data get entity @s Item.components."minecraft:map_decorations"."+".z
scoreboard players set #found rlm_spawn 1
```
suivi du calcul `#x1 = #x - #reach`, `#x2 = #x + #reach`, idem `z`, et de six `execute store result storage rlm_spawn:data lot.<clé> int 1 run scoreboard players get #<clé> rlm_spawn` pour `x, z, x1, z1, x2, z2`.

`step/forceload_area` (macro, quatre quadrants pour rester sous 256 chunks par commande) ; `step/unforceload_area` est identique avec `remove`
```mcfunction
$forceload add $(x1) $(z1) $(x) $(z)
$forceload add $(x) $(z1) $(x2) $(z)
$forceload add $(x1) $(z) $(x) $(z2)
$forceload add $(x) $(z) $(x2) $(z2)
```
`step/wait_area` (macro)
```mcfunction
scoreboard players add #timer rlm_spawn 1
execute if score #timer rlm_spawn matches 6000.. run return run function rlm_spawn:fail
$execute positioned $(x) -64 $(z) as @e[type=minecraft:marker,tag=rlm_spawn.anchor,dx=0,dy=448,dz=0,limit=1] at @s align xyz if function rlm_spawn:generated/area_loaded run function rlm_spawn:step/place
```
`step/place` (exécutée par l'ancre, sur son bloc)
```mcfunction
execute store result score #yaw rlm_spawn run data get entity @s Rotation[0]
scoreboard players operation #yaw rlm_spawn += #c360 rlm_spawn
scoreboard players operation #yaw rlm_spawn %= #c360 rlm_spawn
execute if score #yaw rlm_spawn matches 315.. run function rlm_spawn:generated/place_none
execute if score #yaw rlm_spawn matches ..45 run function rlm_spawn:generated/place_none
execute if score #yaw rlm_spawn matches 46..135 run function rlm_spawn:generated/place_clockwise_90
execute if score #yaw rlm_spawn matches 136..225 run function rlm_spawn:generated/place_clockwise_180
execute if score #yaw rlm_spawn matches 226..314 run function rlm_spawn:generated/place_counterclockwise_90
gamerule spawnRadius 0
function rlm_spawn:step/unforceload_area with storage rlm_spawn:data lot
scoreboard players set #state rlm_spawn 3
```
`step/set_spawn` (macro, positionnée sur le point de spawn)
```mcfunction
$setworldspawn ~ ~ ~ $(yaw)
summon minecraft:marker ~ ~ ~ {Tags:["rlm_spawn.tmp"]}
execute store result storage rlm_spawn:data spawn.x int 1 run data get entity @e[type=minecraft:marker,tag=rlm_spawn.tmp,limit=1] Pos[0]
execute store result storage rlm_spawn:data spawn.y int 1 run data get entity @e[type=minecraft:marker,tag=rlm_spawn.tmp,limit=1] Pos[1]
execute store result storage rlm_spawn:data spawn.z int 1 run data get entity @e[type=minecraft:marker,tag=rlm_spawn.tmp,limit=1] Pos[2]
kill @e[type=minecraft:marker,tag=rlm_spawn.tmp]
```
`arrive` (macro)
```mcfunction
$execute in minecraft:overworld run tp @s $(x) $(y) $(z) $(yaw) 0
tag @s add rlm_spawn.arrived
```
`respawned`
```mcfunction
scoreboard players set @s rlm_spawn.deaths 0
execute unless data entity @s SpawnX run function rlm_spawn:arrive with storage rlm_spawn:data spawn
```
`fail`
```mcfunction
scoreboard players set #state rlm_spawn -2
execute in minecraft:overworld run forceload remove 0 0
execute if data storage rlm_spawn:data lot.x1 in minecraft:overworld run function rlm_spawn:step/unforceload_area with storage rlm_spawn:data lot
```
`warn`
```mcfunction
tellraw @s {"text":"[Royaume de Loutre Mer] Structure de départ introuvable : le spawn reste normal.","color":"yellow"}
tag @s add rlm_spawn.warned
```

- [ ] **Step 5:** Tests verts, `python tools/build_jar.py` produit le jar, commit `Ajoute le repère de génération et la pose au premier chargement`.

### Task 6: Test sur serveur sans interface

**Accord préalable requis de l'utilisateur, à demander avant le Step 2 :** télécharger `server.jar` 1.21.1 (environ 50 Mo) depuis les serveurs officiels de Mojang, et accepter la licence Minecraft (`eula=true`). Sans cet accord, sauter les Steps 2 à 5 et le dire clairement dans le compte rendu.

**Files:**
- Create: `tools/server_test.py`
- Non committé : `tools/.server/`

**Interfaces:**
- Consumes: `tools/build_jar.build_jar`.
- Produces: `python tools/server_test.py --java <java.exe> --seed <texte> [--biome <id>] [--existing-world]`, code de sortie 0 si toutes les vérifications passent, une ligne `PASS`/`FAIL` par vérification.

Fonctionnement : dossier `tools/.server/run-<seed>/` neuf ; `eula.txt` copié depuis `tools/.server/eula.txt` (le script refuse de démarrer s'il manque) ; `server.properties` avec `level-seed`, `online-mode=false`, `server-port=25599` ; le jar copié en `world/datapacks/rlm.zip` (`--biome` réécrit le tag de biome dans cette copie) ; lancement `java -Xmx2G -jar ../server.jar nogui` ; commandes envoyées sur l'entrée standard, réponses lues dans la sortie ; attente de `Done (`, puis `scoreboard players get #state rlm_spawn` toutes les 5 s jusqu'à une valeur hors `1`/`2` (limite 10 min) ; `stop` à la fin.

Vérifications du mode normal :
1. `#state` vaut `3`.
2. `#verified` vaut `1`.
3. `data get storage rlm_spawn:data` contient `lot` et `spawn` ; noter `lot.rotation`.
4. `execute in minecraft:overworld positioned <spawn> if biome ~ ~ ~ minecraft:plains` répond `Test passed`.
5. `execute in minecraft:overworld positioned <spawn> if block ~ ~-1 ~ minecraft:oak_planks` répond `Test passed`.
6. `locate structure rlm_spawn:spawn_lot` renvoie les `x`/`z` de `lot`.
7. `forceload query` ne liste aucun chunk.
8. Second démarrage du même monde : `#state` vaut `3` immédiatement et `spawn` est inchangé.

Mode `--biome minecraft:the_void` : `#state` vaut `-2`, `forceload query` ne liste aucun chunk.
Mode `--existing-world` : premier démarrage sans le datapack, attente de 700 ticks (`time query gametime`), arrêt, ajout du datapack, redémarrage : `#state` vaut `-1`, et `SpawnX`/`SpawnY`/`SpawnZ` lus dans `world/level.dat` avec `nbtio` sont identiques avant et après.

- [ ] **Step 1:** Écrire `tools/server_test.py`.
- [ ] **Step 2:** Après accord : récupérer l'URL et le sha1 de `server.jar` 1.21.1 dans `https://piston-meta.mojang.com/mc/game/version_manifest_v2.json`, télécharger dans `tools/.server/server.jar`, vérifier le sha1. L'utilisateur crée `tools/.server/eula.txt`.
- [ ] **Step 3:** Mode normal sur les seeds `rlm-1`, `rlm-2`, `rlm-3`, `rlm-4`. Attendu : tout `PASS` ; noter les rotations rencontrées (en viser au moins deux différentes, ajouter des seeds sinon).
- [ ] **Step 4:** Modes `--biome minecraft:the_void` et `--existing-world`. Attendu : tout `PASS`.
- [ ] **Step 5:** En cas d'échec : lire `logs/latest.log`, corriger la Tâche 4 ou 5 concernée, relancer **toutes** les seeds. Points fragiles connus à regarder d'abord : ancre absente (`lot.nbt` sans bloc refusé à la pose → y mettre un bloc `minecraft:structure_void` et l'ignorer par processeur), clé `"+"` de la carte, lecture de `Rotation[0]`.
- [ ] **Step 6:** Commit `Ajoute le test sur serveur sans interface`.

### Task 7: Mode d'emploi, installation et vérification en jeu

**Files:**
- Create: `README.md`
- Hors dépôt : `…/Cobblemon Royaume de Loutre Mer 0.2.1 (1)/mods/royaume-loutre-mer-datapack-0.1.0.jar` (après accord)

- [ ] **Step 1:** `README.md` en français : ce que fait le pack ; changer le biome (le fichier de tag) ; changer de build (remplacer le `.litematic`, régler `ground_layer`, `spawn`, `spawn_yaw`, relancer le convertisseur puis `build_jar.py`) ; installer (jar dans `mods/`, et rappel que les starters du dépôt deviennent actifs) ; limites (clairières vides, retour de l'End sur le toit, taille maximale 224 blocs de côté, une seule région).
- [ ] **Step 2:** Commit `Documente le spawn dans la structure`.
- [ ] **Step 3:** Avec l'accord de l'utilisateur, copier le jar dans le `mods/` du pack.
- [ ] **Step 4:** Remettre à l'utilisateur la liste de vérification en jeu :
  1. Nouveau monde : après quelques secondes, on est téléporté à l'intérieur du build.
  2. F3 : le biome est `minecraft:plains`.
  3. Le terrain se raccorde autour du build, sans falaise coupée net.
  4. Mourir sans lit : on revient à l'intérieur, pas sur le toit.
  5. Dormir ailleurs puis mourir : on revient au lit.
  6. Quitter et revenir : pas de nouvelle téléportation.
  7. Ouvrir « New World » : son spawn n'a pas changé.
