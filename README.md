# Datapack Royaume de Loutre Mer

Datapack du modpack « Cobblemon Royaume de Loutre Mer » (Fabric, Minecraft 1.21.1).
Il contient les starters Cobblemon (`data/cobblemon/starters/`) et le spawn dans
la structure de départ (`data/rlm_spawn/`).

## Installation

Construire le jar puis le poser dans le dossier `mods/` du pack :

```bash
python tools/build_jar.py
```

Le jar est écrit dans `build/`. Il active tout le datapack : le spawn **et** les
starters RLM.

## Le spawn dans la structure

À la création d'un monde, le jeu prépare des terrains aplanis dans le biome
choisi. Au premier chargement, le datapack prend celui qui est le plus proche du
centre du monde, y pose le build une seule fois, y place le point d'apparition et
y envoie chaque nouveau joueur. Après une mort sans lit, on revient à l'intérieur.

- Seuls les mondes tout neufs sont concernés : un monde déjà existant n'est
  jamais modifié (son spawn ne bouge pas).
- Si aucun terrain n'est trouvé, le spawn reste normal et un message le signale.
- `/locate structure rlm_spawn:spawn_lot` retrouve l'emplacement.

### Changer le biome

Un seul fichier : `data/rlm_spawn/tags/worldgen/biome/has_structure/spawn_lot.json`.
Garder une seule valeur (par exemple `"minecraft:ocean"` ou un biome de mod).

### Changer le build

1. Remplacer `tools/source/base.litematic` par le nouveau fichier Litematica
   (une seule région, 224 blocs de côté au maximum).
2. Régler `tools/spawn_base.json` (coordonnées comptées depuis le coin du build
   une fois les couches vides retirées) :
   - `ground_layer` : couche du build posée au niveau du sol du terrain ; les
     couches du dessous sont enterrées ;
   - `spawn` : `[x, y, z]` du bloc où l'on apparaît (2 blocs d'air, un bloc
     solide dessous) ;
   - `spawn_yaw` : direction du regard en degrés.
3. Régénérer puis reconstruire le jar :

```bash
python tools/convert_spawn_base.py
```

```bash
python tools/build_jar.py
```

Le convertisseur avertit si le build contient des blocs de mods ou vient d'une
version plus récente que 1.21.1. Les fichiers de `data/rlm_spawn/structure/` et
`data/rlm_spawn/function/generated/` sont régénérés : ne pas les éditer à la main.

### Limites connues

- D'autres terrains préparés existent ailleurs dans le même biome : ce sont des
  clairières plates et vides, espacées d'environ 1 000 blocs. Elles apparaissent
  aussi dans les nouvelles zones des mondes existants.
- Le build est orienté au hasard d'un monde à l'autre.
- Au retour de l'End sans lit, le jeu fait réapparaître sur le toit.

## Tests

```bash
python -m unittest discover -s tools/tests -v
```

Test sur un vrai serveur 1.21.1 (nécessite `tools/.server/server.jar` et
`tools/.server/eula.txt`, non committés) :

```bash
python tools/server_test.py --java <chemin vers java.exe> --seed rlm-1
```

Options : `--biome minecraft:the_void` (biome introuvable) et `--existing-world`
(monde déjà existant).
